# -*- coding: utf-8 -*-
import io
import logging
import os
import re
import shutil
import tempfile
import zipfile

import requests

from odoo import _, addons, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.modules.module import get_module_path
from odoo.tools import config
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)

PAGE_SIZE = 200
HTTP_TIMEOUT = 20
MAX_ZIP_BYTES = 100 * 1024 * 1024
MODULE_RE = re.compile(r'^[a-z0-9_]+$')
DEFAULT_ICON = '/base/static/description/icon.png'


class CylloStoreApp(models.Model):
    """Local cache of the apps published on apps.cyllo.com.

    Rows are refreshed every time the "Cyllo App Store" menu is opened and
    are shown in a kanban that looks like the standard Apps one.
    """
    _name = 'cyllo.store.app'
    _description = 'Cyllo Store App'
    _order = 'top_apps desc, download_count desc, name'

    PANEL_TYPES = [('official', 'Official Apps'),
                   ('industries', 'Industries'),
                   ('cyllo_store', 'Cyllo App Store')]

    name = fields.Char(required=True, readonly=True)
    remote_id = fields.Integer(required=True, readonly=True, index=True)
    technical_name = fields.Char(readonly=True, index=True)
    summary = fields.Text(readonly=True)
    version = fields.Char(readonly=True)
    author = fields.Char(readonly=True)
    category = fields.Char(readonly=True)
    category_id = fields.Many2one('cyllo.store.category', readonly=True)
    panel_type = fields.Selection(PANEL_TYPES, default='cyllo_store',
                                  required=True, readonly=True)
    license = fields.Char(readonly=True)
    website = fields.Char(readonly=True)
    live_test_url = fields.Char(readonly=True)
    depends = fields.Char(readonly=True)
    icon_url = fields.Char(readonly=True)
    top_apps = fields.Boolean(readonly=True)
    verified = fields.Boolean(readonly=True)
    download_count = fields.Integer(readonly=True)
    is_installed = fields.Boolean(compute='_compute_is_installed',
                                  search='_search_is_installed')

    _sql_constraints = [
        ('remote_id_uniq', 'unique(remote_id)',
         'This store app is already cached.'),
    ]

    # ------------------------------------------------------------------
    # installed state
    # ------------------------------------------------------------------
    def _installed_names(self):
        """Return the technical names of installed or pending modules."""
        return set(self.env['ir.module.module'].sudo().search(
            [('state', 'in', ('installed', 'to install', 'to upgrade'))]
        ).mapped('name'))

    @api.depends('technical_name')
    def _compute_is_installed(self):
        """Compute whether each App Store application is installed locally."""
        installed = self._installed_names()
        for app in self:
            app.is_installed = app.technical_name in installed

    def _search_is_installed(self, operator, value):
        """Build a search domain for the application installation status."""
        if operator not in ('=', '!='):
            raise UserError(_('Unsupported operator.'))
        positive = (operator == '=') == bool(value)
        return [('technical_name', 'in' if positive else 'not in',
                 list(self._installed_names()))]

    # ------------------------------------------------------------------
    # configuration
    # ------------------------------------------------------------------
    @api.model
    def _store_base_url(self):
        """Return the configured Cyllo App Store base URL."""
        url = self.env['ir.config_parameter'].sudo().get_param(
            'cyllo_store.base_url', 'https://apps.cyllo.com')
        return (url or '').rstrip('/')

    @api.model
    def _target_dir(self):
        """Folder the downloaded modules are extracted into.

        Order: the 'cyllo_store.addons_dir' parameter (no fallback), else the
        folder holding this module, else a 'marketplace' folder next to it,
        else '<data_dir>/marketplace_addons' (the data dir is normally the
        one place the Odoo user can always write to).
        """
        param = self.env['ir.config_parameter'].sudo().get_param('cyllo_store.addons_dir')
        if param:
            candidates = [param]
        else:
            parent = os.path.dirname(get_module_path('cyllo_store_client'))
            candidates = [
                parent,
                os.path.join(os.path.dirname(parent), 'marketplace'),
                os.path.join(config['data_dir'], 'marketplace_addons'),
            ]
        known = {os.path.realpath(p) for p in addons.__path__}
        problems = []
        for path in candidates:
            path = os.path.realpath(path)
            try:
                os.makedirs(path, exist_ok=True)
            except OSError as exc:
                problems.append('%s (%s)' % (path, exc.strerror))
                continue
            if not os.access(path, os.W_OK):
                problems.append('%s (not writable)' % path)
                continue
            if path not in known:
                # visible to this process right away; to survive restarts and
                # other workers the folder must also be in addons_path
                addons.__path__.append(path)
                _logger.warning("Cyllo store: %s is not in addons_path, "
                                "add it to the server configuration.", path)
            return path
        raise UserError(_("No writable folder found for new apps. Tried: %s",
                          '; '.join(problems)))

    # ------------------------------------------------------------------
    # sync
    # ------------------------------------------------------------------
    @api.model
    def _fetch_remote_apps(self):
        """Fetch all published applications from the remote Cyllo App Store."""
        base = self._store_base_url()
        apps, offset = [], 0
        while True:
            try:
                resp = requests.get(
                    base + '/cyllo_store/api/apps',
                    params={'limit': PAGE_SIZE, 'offset': offset},
                    timeout=HTTP_TIMEOUT)
                resp.raise_for_status()
                data = resp.json()
            except (requests.RequestException, ValueError) as exc:
                raise UserError(_("Could not reach the Cyllo App Store "
                                  "(%s): %s", base, exc))
            batch = data.get('apps') or []
            apps.extend(batch)
            offset += len(batch)
            if not batch or offset >= data.get('total', 0):
                return apps

    @api.model
    def _sync_from_store(self):
        base = self._store_base_url()
        remote = self._fetch_remote_apps()
        existing = {a.remote_id: a for a in self.sudo().search([])}
        Category = self.env['cyllo.store.category'].sudo()
        categories = {c.name: c for c in Category.search([])}
        seen = set()
        for item in remote:
            tech = item.get('technical_name') or ''
            if not MODULE_RE.match(tech):
                continue  # never trust a name that ends up in a file path
            icon = item.get('icon_url')
            cat_name = (item.get('category') or '').split('/', 1)[-1].strip()
            if cat_name and cat_name not in categories:
                categories[cat_name] = Category.create({'name': cat_name})
            vals = {
                'category_id': categories[cat_name].id if cat_name else False,
                'name': item.get('name') or tech,
                'remote_id': item['id'],
                'technical_name': tech,
                'summary': item.get('summary'),
                'version': item.get('version'),
                'author': item.get('author'),
                'category': item.get('category'),
                'license': item.get('license'),
                'website': item.get('website'),
                'live_test_url': item.get('live_test_url'),
                'depends': ', '.join(item.get('depends') or []),
                'top_apps': item.get('top_apps'),
                'verified': bool(item.get('verified')),
                'download_count': item.get('download_count'),
                'icon_url': (base + icon) if icon else DEFAULT_ICON,
            }
            seen.add(item['id'])
            if item['id'] in existing:
                existing[item['id']].write(vals)
            else:
                self.sudo().create(vals)
        # unpublished on the store -> gone here too
        stale = [a.id for rid, a in existing.items() if rid not in seen]
        if stale:
            self.sudo().browse(stale).unlink()

    @api.model
    def search_panel_select_range(self, field_name, **kwargs):
        res = super().search_panel_select_range(field_name, **kwargs)
        if field_name == 'panel_type':  # always list the 3 entries
            res['values'] = [{'id': key, 'display_name': label}
                             for key, label in self.PANEL_TYPES]
        return res

    @api.model
    def action_open_apps(self, module_type=False):
        """Back to the standard Apps kanban, optionally on the Official Apps
        or Industries entry of its left panel."""
        try:
            action = self.env['ir.actions.act_window']._for_xml_id(
                'base.open_module_tree')
        except ValueError:
            action = {'type': 'ir.actions.act_window', 'name': _('Apps'),
                      'res_model': 'ir.module.module',
                      'views': [(False, 'kanban'), (False, 'tree'),
                                (False, 'form')]}
        context = action.get('context') or {}
        if isinstance(context, str):
            try:
                context = safe_eval(context)
            except Exception:
                context = {}
        context = dict(context)
        if module_type:
            context['searchpanel_default_module_type'] = module_type
        action['context'] = context
        return action

    @api.model
    def action_open_store(self):
        """Refresh the cache, then open the kanban. If the store is
        unreachable the last cached list is shown instead of an error."""
        if not self.env.user.has_group('base.group_system'):
            raise AccessError(_("Only administrators can use the Cyllo "
                                "App Store."))
        try:
            self._sync_from_store()
        except UserError:
            if not self.sudo().search_count([]):
                raise
            _logger.warning("Cyllo App Store unreachable, showing cached list",
                            exc_info=True)
        return self.env['ir.actions.act_window']._for_xml_id(
            'cyllo_store_client.action_cyllo_store_app')

    # ------------------------------------------------------------------
    # buttons
    # ------------------------------------------------------------------
    def action_learn_more(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_url', 'target': 'new',
                'url': '%s/apps/%s' % (self._store_base_url(),
                                       self.technical_name)}

    def _download_zip(self):
        url = '%s/cyllo_store/api/download/%s' % (self._store_base_url(),
                                                  self.remote_id)
        try:
            with requests.get(url, stream=True, timeout=HTTP_TIMEOUT) as resp:
                resp.raise_for_status()
                buf, size = io.BytesIO(), 0
                for chunk in resp.iter_content(1024 * 256):
                    size += len(chunk)
                    if size > MAX_ZIP_BYTES:
                        raise UserError(_("The download is too large."))
                    buf.write(chunk)
        except requests.RequestException as exc:
            raise UserError(_("Download failed: %s", exc))
        buf.seek(0)
        return buf

    @api.model
    def _extract_zip(self, buf, target):
        """Extract the top-level module folders of `buf` into `target`.
        Existing folders are never overwritten. Returns the new folders."""
        try:
            zf = zipfile.ZipFile(buf)
        except zipfile.BadZipFile:
            raise UserError(_("The downloaded file is not a valid zip."))
        created = []
        tmp = tempfile.mkdtemp(dir=target, prefix='.cyllo_store_')
        try:
            root = os.path.realpath(tmp)
            with zf:
                for member in zf.infolist():  # zip-slip guard
                    dest = os.path.realpath(os.path.join(tmp, member.filename))
                    if dest != root and not dest.startswith(root + os.sep):
                        raise UserError(_("Unsafe path in the downloaded "
                                          "archive."))
                zf.extractall(tmp)
            for entry in sorted(os.listdir(tmp)):
                src = os.path.join(tmp, entry)
                dst = os.path.join(target, entry)
                if (not os.path.isdir(src) or not MODULE_RE.match(entry)
                        or os.path.exists(dst)):
                    continue
                shutil.move(src, dst)
                created.append(entry)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        return created

    def action_install(self):
        """Download the app (and its store dependencies), refresh the module
        list and install it."""
        self.ensure_one()
        if not self.env.user.has_group('base.group_system'):
            raise AccessError(_("Only administrators can install apps."))
        if self.is_installed:
            raise UserError(_("%s is already installed.", self.name))
        target = self._target_dir()
        created = self._extract_zip(self._download_zip(), target)
        _logger.info("Cyllo store: extracted %s into %s", created, target)
        Module = self.env['ir.module.module']
        Module.update_list()
        module = Module.search([('name', '=', self.technical_name)], limit=1)
        if not module:
            raise UserError(_("%s was downloaded but Odoo does not list it as "
                              "a module. Check the server log.", self.name))
        return module.button_immediate_install()
