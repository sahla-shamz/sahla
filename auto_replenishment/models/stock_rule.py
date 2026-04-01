# -*- coding: utf-8 -*-

from odoo import models, api
from collections import defaultdict, OrderedDict

class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _search_rule_for_warehouses(self, route_ids, packaging_uom_id, product_id, warehouse_ids, domain):
        res= super()._search_rule_for_warehouses(route_ids, packaging_uom_id, product_id, warehouse_ids, domain)
        sale_order= self.env['sale.order'].search([], order="id desc", limit=1)

        for line in sale_order.order_line:
            production_time = line.product_id.bom_ids.produce_delay
            vendor_delivery_lead_time = [i.delay for i in line.product_id.seller_ids][0]


            if ((line.product_id.qty_available > line.product_id.available_threshold and
                    "Buy" in line.product_id.route_ids.mapped("name") and
                    "Manufacture" in line.product_id.route_ids.mapped("name")) and
                    production_time > vendor_delivery_lead_time ):
                man_route= line.product_id.route_ids.filtered(lambda l : l.name == "Manufacture")


                result = self.env["stock.rule"]._read_group(
                    domain,
                    groupby=["location_dest_id", "warehouse_id", "route_id"],
                    aggregates=["id:recordset"],
                    order="route_sequence:min, sequence:min",
                )
                for route  in result:
                    if man_route in route :
                        result.remove(route)

                rule_dict = defaultdict(OrderedDict)
                for group in result:
                    rule_dict[group[0].id, group[2].id][group[1].id] = group[3].sorted(lambda rule: (rule.route_sequence, rule.sequence))[0]
                res= rule_dict
        return res