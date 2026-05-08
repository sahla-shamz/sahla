from odoo import fields, models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"


    is_created_from_pos = fields.Boolean("Created from poS", readonly=True)
    pos_session_id = fields.Many2one("pos.session", string="POS Session", readonly=True)


    @api.model
    def create_sale_order(self, state, product_id, partner_id, note, session):
        print("hhhhh", state)
        print("hhhhh", product_id)
        print("hhhhh", partner_id)


        sale_order = self.create({
            'partner_id': partner_id,
            'state' : state,
            'note' : note,
            'is_created_from_pos' : True,
            'pos_session_id' : session,
            'order_line' : [fields.Command.create({
                'product_id': pro['id'],
                'product_uom_qty': pro['qty'],
                'price_unit': pro['price'],
                'tax_ids' : [fields.Command.set(pro['tax'])],
            }) for pro in product_id],


        })


        print('sale Order', sale_order)



        return sale_order.name