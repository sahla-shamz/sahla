from odoo.addons.website_sale.controllers.main import WebsiteSale



class WebsiteSaleForm(WebsiteSale):


    def _shop_lookup_products(self, options, post, search, website):

        fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(options, post, search, website)

        # if self.env.user.product_ids:
        #     search_result = self.env.user.product_ids
        # elif self.env.user.product_category_ids:
        #     search_result = self.env['product.template'].search([('public_categ_ids', 'in', self.env.user.product_category_ids.ids )])


        product_count = len(search_result)

        return fuzzy_search_term, product_count, search_result



    def _get_additional_shop_values(self, values, **kwargs):

        if self.env.user.product_ids:
            categs= self.env.user.product_ids.public_categ_ids
            values['categories'] = categs
            values['category_entries'] = categs

        if self.env.user.product_category_ids:
            categs = self.env.user.product_category_ids
            values['categories'] = categs
            values['category_entries'] = categs

        res= super()._get_additional_shop_values(values, **kwargs)

        return res
