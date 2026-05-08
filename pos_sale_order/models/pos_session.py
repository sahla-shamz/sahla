from odoo import api, fields, models, tools

class PosSession(models.Model):
    _inherit = 'pos.session'

    sale_order_ids = fields.One2many("sale.order", "pos_session_id", string="Sales Orders")
    sale_count= fields.Integer(string="Sales Order Count", compute="_compute_sale_count")


    @api.depends('sale_order_ids')
    def _compute_sale_count(self):
        for rec in self:
            rec.sale_count = len(rec.sale_order_ids)



    def action_sale_list(self):
        return {
            "name" : "Sale Orders",
            "type" : "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "sale.order",
            "domain" : [('pos_session_id', '=', self.id)]
        }