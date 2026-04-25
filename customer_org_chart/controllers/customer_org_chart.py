from odoo import http


class CustomerOrgChart(http.Controller):

    @http.route('/customer/get_org_chart', type='jsonrpc', auth='user')
    def get_org_chart(self, employee_id):
        print("customer_org_chart controller")
        print("employeee",employee_id)
        partner = self.env['res.partner'].browse(employee_id)
        print("partner",partner)
        if partner.is_child:
            manager = {
                'id' : partner.parent_partner_id.id,
                'name' : partner.parent_partner_id.name,
                'is_child' : partner.is_child,
                'is_parent' : partner.is_parent,
            }

            children=[]
            for child in partner.parent_partner_id.customer_child_ids:
                child ={
                    'id' : child.id,
                    'name' : child.name,
                    'is_child' : child.is_child,
                    'is_parent' : child.is_parent,
                    'write_date' : child.write_date,
                }
                children.append(child)
            print("children",children)

        elif partner.is_parent:
            manager = {
                'id' : partner.id,
                'name' : partner.name,
                'is_child' : partner.is_child,
                'is_parent' : partner.is_parent,
                "write_date" : partner.write_date,
            }
            # children = partner.customer_child_ids
            children = []

            for child_id in partner.customer_child_ids:
                print("child_id",child_id)

                child= {
                    'id' : child_id.id,
                    'name' : child_id.name,
                    'is_child' : child_id.is_child,
                    'is_parent' : child_id.is_parent,
                    'write_date' : child_id.write_date,
                }
                children.append(child)
            print(children)


        else:
            manager = {}

            children = {}

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
