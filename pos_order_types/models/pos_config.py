# -*- coding: utf-8 -*-

from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    order_type_id = fields.Many2many("pos.order.type", string="Order Type")
    is_enable_order_type = fields.Boolean(string="Enable Order Type")
