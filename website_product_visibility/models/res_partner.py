# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"


    select_pro_cat= fields.Selection([('products', "Products"), ('category', "Product Category")],
                                     string="Product or Category")
    product_ids = fields.Many2many("product.template", string="Products")
    product_category_ids = fields.Many2many("product.public.category", string="Categories",
                                            domain="[['parent_id', '=', False]]")
    is_product = fields.Boolean(string="Is Product", compute="_compute_is_product")
    is_category = fields.Boolean(string="Is Category")


    @api.depends('select_pro_cat')
    def _compute_is_product(self):
        """Compute the boolean values to display the category and product field based on the selection"""
        for rec in self:
            if rec.select_pro_cat == 'products':
                self.update({
                    'product_category_ids' : [fields.Command.clear()]
                })
                rec.is_product = True
                rec.is_category = False
            elif rec.select_pro_cat == 'category':
                self.update({
                    'product_ids': [fields.Command.clear()]
                })
                rec.is_category = True
                rec.is_product = False
            else:
                rec.is_product = False
                rec.is_category = False


