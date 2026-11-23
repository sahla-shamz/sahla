# -*- coding: utf-8 -*-
from odoo import _, api, models


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    @api.model
    def search_panel_select_range(self, field_name, **kwargs):
        res = super().search_panel_select_range(field_name, **kwargs)
        if field_name == 'module_type':
            values = res.get('values')
            if values is not None:
                entry = {'id': 'cyllo_store',
                         'display_name': _('Cyllo App Store')}
                # keep the same shape as the existing entries
                if values and '__count' in values[0]:
                    entry['__count'] = 0
                values.append(entry)
        return res