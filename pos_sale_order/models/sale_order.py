from odoo import fields, models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"



    def create_sale_order(self, option_value):
        print("hhhhh", option_value)

        return True