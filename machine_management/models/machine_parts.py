# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools

class MachineParts(models.Model):
    _name = 'machine.parts'
    _description = 'Machine Parts'

    service_id=fields.Many2one(comodel_name='machine.service',string="Service")
    product_id = fields.Many2one(comodel_name='product.product',string="Machine Part")
    quantity = fields.Integer(string="Quantity", default=1)
    uom_id=fields.Many2one(comodel_name='uom.uom',string="Unit of measures", compute='_compute_uom_id', store=True, readonly=False)
    machine_id=fields.Many2one(comodel_name='machine.management.machine',string="Machine")
    price_unit = fields.Float(
        string="Unit Price",
        compute='_compute_price_unit',
        store=True, readonly=False, required=True)
    amount=fields.Float(string="Amount", compute='_compute_amount', store=True)

    tags= fields.Many2many(comodel_name='machine.tags',string="Tags")

    @api.depends('product_id')
    def _compute_uom_id(self):
        for record in self:
            record.uom_id = record.product_id.uom_id

    @api.depends('product_id')
    def _compute_price_unit(self):
        for record in self:
            record.price_unit = record.product_id.list_price

    @api.depends('price_unit','quantity')
    def _compute_amount(self):
        for record in self:
            record.amount= record.price_unit * record.quantity


