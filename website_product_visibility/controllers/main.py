# -*- coding: utf-8 -*-

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleForm(WebsiteSale):

    def _get_additional_shop_values(self, values, **kwargs):
        """Editing the categories return by the values of shop to display on the shop page"""
        if not values['category']:
            if self.env.user.product_ids:
                categs = self.env.user.product_ids.public_categ_ids.filtered(lambda l : not l.parent_id)
                categs = categs + self.env.user.product_ids.public_categ_ids.filtered(lambda l : l.parent_id).parent_id
                values['categories'] = set(categs)
                values['category_entries'] = set(categs)

            elif self.env.user.product_category_ids:
                categs = self.env.user.product_category_ids
                values['category_entries'] = categs
                values['categories'] = categs
            else:
                values['category_entries'] = False

        return super()._get_additional_shop_values(values, **kwargs)

