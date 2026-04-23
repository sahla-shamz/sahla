# -*- coding: utf-8 -*-

from odoo import models


class WebsiteSearchableMixin(models.AbstractModel):
    _inherit = 'website.searchable.mixin'


    def _search_build_domain(self, domain_list, search, fields, extra=None):
        """Super the domain to show only the allowed products on the webpage so the search bar, attributes,
         and products get filtered out"""
        if self.env.user.product_category_ids:
            domain_list.append(['|',('id', 'in', self.env.user.product_category_ids.product_tmpl_ids.ids),
                                ('id', 'in', self.env.user.product_category_ids.child_id.product_tmpl_ids.ids)])
        elif self.env.user.product_ids:
            domain_list.append([('id', 'in', self.env.user.product_ids.ids)])

        else:
            domain_list.append([('id', '=', False)])

        res= super()._search_build_domain(domain_list, search, fields, extra= None)
        return res
