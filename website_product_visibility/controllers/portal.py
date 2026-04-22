from odoo import http
from odoo.http import request

class Portal(http.Controller):

    @http.route(['/my/products'], type='http', auth="public", website=True)
    def my_products(self):

        if self.env.user.product_ids:
            data ={'products' : self.env.user.product_ids}
        elif self.env.user.product_category_ids:
            data = {'products': self.env.user.product_category_ids.product_tmpl_ids.filtered(lambda l : l.is_published)
                    + self.env.user.product_category_ids.child_id.product_tmpl_ids.filtered(lambda l : l.is_published)}

        print(data['products'])
        data['page_name'] = 'my_products'


        return request.render("website_product_visibility.portal_my_products", data)


    @http.route(['/product/<int:id>'], type='http', auth="public", website=True)
    def product_detail(self, id):
        print(id)

        product= self.env['product.template'].browse(id)
        print(product)
        return request.redirect(product._get_product_url())

    @http.route(['/product_details/<int:id>'], type='http', auth="public", website=True)
    def product_template(self,id):
        print(id)
        product= self.env['product.template'].browse(id)
        # print(product.image_1920)
        data={'product' : product, 'page_name' : 'product_details'}
        return request.render("website_product_visibility.product_template", data)



