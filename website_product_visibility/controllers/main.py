from odoo.addons.website_sale.controllers.main import WebsiteSale



class WebsiteSaleForm(WebsiteSale):


    def _get_additional_shop_values(self, values, **kwargs):

        if not values['category']:
            if self.env.user.product_ids:
                print(self.env.user.product_ids.public_categ_ids.filtered(lambda l : not l.parent_id))
                categs = self.env.user.product_ids.public_categ_ids.filtered(lambda l : not l.parent_id)
                categs = categs + self.env.user.product_ids.public_categ_ids.filtered(lambda l : l.parent_id).parent_id
                values['categories'] = categs
                values['category_entries'] = categs

            elif self.env.user.product_category_ids:
                categs = self.env.user.product_category_ids
                values['category_entries'] = categs
                values['categories'] = categs
            else:

                values['category_entries'] = False
        res= super()._get_additional_shop_values(values, **kwargs)

        return res
