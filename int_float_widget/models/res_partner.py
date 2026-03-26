# -*- coding: utf-8 -*-

from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    custom_field=fields.Float(string="Custom Field")