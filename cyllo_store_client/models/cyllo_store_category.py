# -*- coding: utf-8 -*-
from odoo import fields, models


class CylloStoreCategory(models.Model):
    _name = 'cyllo.store.category'
    _description = 'Cyllo Store Category'
    _order = 'name'

    name = fields.Char(required=True, readonly=True)
