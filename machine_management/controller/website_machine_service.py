from odoo import http
from odoo.http import request

class WebsiteMachineServiceForm(http.Controller):
    @http.route('/machine_service', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def machine_service_form(self, **kw):
        """Render the Machine service form"""
        machines = request.env['machine.management.machine'].sudo().search([])
        customers = request.env['res.partner'].sudo().search([])
        data ={
            'machines': machines,
            'customers': customers,
        }

        return request.render('machine_management.machine_service_website_form_template', data)

    @http.route('/website/machine_service/create', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def create_machine_service(self, **post):
        """Handle form submission and create a new machine service"""
        machine_id = post.get('machine')
        description = post.get('description')
        customer_id = post.get('customer')
        date=post.get('date')
        if not machine_id:
            # If name is missing, redirect back to form with an error message
            return request.render('machine_management.machine_service', {
                'error': 'Name is required!'
            })
        request.env['machine.service'].sudo().create({
            'machine_id': machine_id,
            'description': description,
            'customer_id': customer_id,
            'date': date,

        })
        return request.render('machine_management.machine_service_success_template')



