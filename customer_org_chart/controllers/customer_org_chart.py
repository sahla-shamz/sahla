from odoo import http


class CustomerOrgChart(http.Controller):

    @http.route('/customer/get_org_chart', type='jsonrpc', auth='user')
    def get_org_chart(self, employee_id, new_parent_id=None, **kw):
        print("customer_org_chart controller")
        print("employeee",employee_id)
        partner = self.env['res.partner'].browse(employee_id)
        print("partner",partner)
        manager = {
            'id' : partner.parent_partner_id.id,
            'name' : partner.parent_partner_id.name,
            'is_child' : partner.is_child,
            'is_parent' : partner.is_parent,
        }

        children = partner.customer_child_ids

        # values = {
        #     'parent_id': partner,
        #     'child_ids': partner.customer_child_ids,
        # }
        values= {
            'manager' : manager,
            'children' : children,
        }
        print("values",values)
        return values
