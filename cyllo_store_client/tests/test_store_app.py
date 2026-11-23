# -*- coding: utf-8 -*-
import io
import os
import tempfile
import zipfile
from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


def make_zip(files):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        for name, data in files.items():
            zf.writestr(name, data)
    buf.seek(0)
    return buf


class TestCylloStoreApp(TransactionCase):

    def test_sync_upsert_and_remove(self):
        App = self.env['cyllo.store.app']
        payload = [{'id': 1, 'name': 'A', 'technical_name': 'mod_a',
                    'depends': ['base'], 'icon_url': None},
                   {'id': 2, 'name': 'Bad', 'technical_name': '../evil'}]
        with patch.object(type(App), '_fetch_remote_apps', return_value=payload):
            App._sync_from_store()
        self.assertEqual(App.search([]).mapped('technical_name'), ['mod_a'])
        with patch.object(type(App), '_fetch_remote_apps', return_value=[]):
            App._sync_from_store()
        self.assertFalse(App.search([]))

    def test_extract_blocks_zip_slip(self):
        App = self.env['cyllo.store.app']
        with tempfile.TemporaryDirectory() as target:
            with self.assertRaises(UserError):
                App._extract_zip(make_zip({'../evil.py': 'x'}), target)

    def test_extract_skips_existing(self):
        App = self.env['cyllo.store.app']
        with tempfile.TemporaryDirectory() as target:
            os.mkdir(os.path.join(target, 'mod_a'))
            created = App._extract_zip(make_zip({
                'mod_a/__manifest__.py': '{}',
                'mod_b/__manifest__.py': '{}'}), target)
            self.assertEqual(created, ['mod_b'])
