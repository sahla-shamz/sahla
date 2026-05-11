# -*- coding: utf-8 -*-

from odoo import models,fields,api

class PosConfig(models.Model):
    _inherit = "pos.config"

    is_create_sale_order = fields.Boolean(string="Create Sales Order")
