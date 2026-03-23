from odoo import http
from odoo.addons.base.models.ir_qweb import render
from odoo.http import request


class WebsiteCreateCustomer(http.Controller):
    @http.route("/create_customer", type='http', auth='public', website=True, methods=['GET', 'POST'])
    def create_customer(self, **post):
        """Handle form submission renders customer form creation"""
        countries= self.env['res.country'].sudo().search([])
        data = {
            'countries': countries,
        }
        return request.render("machine_management.create_customer_website_form_template", data)


    @http.route("/website/customer/create", type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def create_customer_website_form(self, **post):
        """Handle form submission and create a new customer"""

        name=post.get('name')
        email=post.get('email')
        phone=post.get('phone')
        country_id = post.get('country')
        print(country_id)

        self.env['res.partner'].sudo().create({

            'country_id': country_id,
            'email': email,
            'name': name,
            'phone': phone,

        })

        return request.render("machine_management.customer_create_success_template")