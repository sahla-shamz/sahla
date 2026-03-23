# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class MachineHighlightSnippet(http.Controller):
    @http.route('/get_machines', type='jsonrpc', auth='public',website=True)
    def get_machines(self):
        """Get the first four latest machines"""
        four_machines= request.env['machine.management.machine'].sudo().search_read([], fields=['name', 'image', 'id'], order= "id desc", limit= 12)
        machine_name=[]
        machine_image=[]
        machine_id=[]
        for machine in four_machines:
            machine_name.append(machine['name'])
            machine_image.append(machine['image'])
            machine_id.append(machine['id'])

        return four_machines, machine_name, machine_image, machine_id