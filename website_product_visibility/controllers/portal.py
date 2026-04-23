# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class Portal(http.Controller):

    @http.route(['/my/products'], type='http', auth="public", website=True)
    def my_products(self):
        """Get the allowed products to display to display on the shop page"""
        data ={}
        if self.env.user.product_ids:
            data['products'] = self.env.user.product_ids
        elif self.env.user.product_category_ids:
            data['products']= (self.env.user.product_category_ids.product_tmpl_ids.filtered(lambda l : l.is_published) +
                    self.env.user.product_category_ids.child_id.product_tmpl_ids.filtered(lambda l : l.is_published))

        data['page_name'] = 'my_products'

        return request.render("website_product_visibility.portal_my_products", data)


    @http.route(['/product/<int:id>'], type='http', auth="public", website=True)
    def product_shop(self, id):
        """Navigate to the product shop page on clicking the View button"""
        product= self.env['product.template'].browse(id)
        return request.redirect(product._get_product_url())


    @http.route(['/product_details/<int:id>'], type='http', auth="public", website=True)
    def product_details(self,id):
        """Render to new product template on clicking on the name of the product"""
        product= self.env['product.template'].browse(id)
        data={'product' : product, 'page_name' : 'product_details'}
        return request.render("website_product_visibility.product_template", data)



