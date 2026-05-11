# -*- coding: utf-8 -*-

from odoo import fields, models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"


    is_created_from_pos = fields.Boolean("Created from poS", readonly=True)
    pos_session_id = fields.Many2one("pos.session", string="POS Session", readonly=True)


    @api.model
    def create_sale_order(self, state, product_id, partner_id, note, session, pricelist):
        """Create Sale Order from pos order with arguments passed as orm call from js"""
        sale_order = self.create({
            'partner_id': partner_id,
            'state' : state,
            'note' : note,
            'is_created_from_pos' : True,
            'pos_session_id' : session,
            'pricelist_id' : pricelist,
            'order_line' : [fields.Command.create({
                'product_id': pro['id'],
                'product_uom_qty': pro['qty'],
                'price_unit': pro['price'],
                'tax_ids' : [fields.Command.set(pro['tax'])],
                'discount' : pro['discount'] if 'discount' in pro.keys() else False,
            }) for pro in product_id],

        })

        return sale_order.name
