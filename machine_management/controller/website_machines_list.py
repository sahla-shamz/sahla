from odoo import http
from odoo.http import request

class MachinesController(http.Controller):
    @http.route("/machine_list", type="http", auth="user", website=True)
    def machines_list(self):
        """Renders the machine list template"""
        machines= request.env["machine.management.machine"].sudo().search([])
        data= {
            'machines': machines
        }

        return request.render("machine_management.machine_list_website_template", data)


    @http.route("/machine_overview/<int:website_id>", type="http", auth="public", website=True)
    def machine_overview(self, **post):
        """renders to machine overview template"""
        path=  http.request.httprequest.path
        machine_id= path.split("/")[-1]

        machine= request.env["machine.management.machine"].sudo().browse(int(machine_id))
        data= {'machine': machine}

        return request.render("machine_management.machine_overview_website_template", data)