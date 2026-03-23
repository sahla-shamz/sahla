# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError
import json
from odoo.tools import json_default

class MachineTransferReporting(models.TransientModel):
    _name = 'machine.transfer.reporting'
    _description = 'Reporting'

    from_date= fields.Date(string="From Date")
    to_date= fields.Date(string="To Date")
    partner_id = fields.Many2many('res.partner',"machine_transfer_partner_rel", string="Customer")
    transfer_types= fields.Selection([('install', 'Install'), ('remove', 'Remove')], string="Transfer Type")
    machine_id = fields.Many2many('machine.management.machine',"machine_transfer_machine_rel", string="Machine")



    def query_filter(self):
        params = []

        query = """SELECT mt.seq_number, m.name as machine_name, rp.name, mt.transfer_date, mt.transfer_type, mt.transfer_states, rc.name as company 
                FROM machine_transfer as mt LEFT JOIN res_partner as rp on mt.customer_id = rp.id
                 LEFT JOIN machine_management_machine as m ON mt.machine_id= m.id 
                 JOIN res_company as rc ON mt.company_id = rc.id WHERE """

        if self.partner_id:
            query += 'mt.customer_id in %s AND '
            params.append(tuple(self.partner_id.ids))

        if self.transfer_types:
            query += 'mt.transfer_type = %s AND '
            params.append(self.transfer_types)

        if self.from_date:
            query += 'mt.transfer_date > %s AND '
            params.append(self.from_date)

        if self.to_date:
            query += 'mt.transfer_date < %s AND '
            params.append(self.to_date)

        if self.machine_id:
            query += 'mt.machine_id in %s AND '
            params.append(tuple(self.machine_id.ids))

        new_query = " ".join(query.split()[:-1])
        print("new query",new_query)
        self.env.cr.execute(new_query, params)
        query_set = self.env.cr.dictfetchall()
        if not query_set:
            raise UserError("Machine Transfer reporting: No Machines found")

        return query_set


    def action_print(self):
        query_set= self.query_filter()
        install_list = [dict for dict in query_set if dict['transfer_type'] == 'install']
        remove_list = [dict for dict in query_set if dict['transfer_type'] == 'remove']

        data = {'install_list': install_list,
                'remove_list': remove_list,
                'vals': query_set}

        action = (self.env.ref('machine_management.action_machine_transfer_report').report_action([], data=data))
        action.update({'close_on_report_download': True})
        return action


    def action_print_xls(self):
        data = self.query_filter()
        return {
            'type':'ir.actions.report',
            'data' : {
                'model' : 'machine.transfer.report',
                'options' : json.dumps(data, default=json_default),
                'output_format' : 'xlsx',
                'report_name' : 'Machine Transfer XLS Report'
            },
            'report_type' : 'xlsx',

        }




    # def get_xlsx_report(self, data, response):
    #     print("getting xlsx report")
    #     docs= self.query_filter()
    #     output = io.BytesIO()
    #     workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    #     print("workbook", workbook)
    #     sheet = workbook.add_worksheet()
    #
    #     border = workbook.add_format({'border': 1})
    #     cell_format = workbook.add_format(
    #         {'font_size': '12px', 'align': 'center'})
    #     head = workbook.add_format(
    #         {'align': 'center', 'bold': True, 'font_size': '20px'})
    #     date_size = workbook.add_format(
    #         {'font_size': 12, 'bold': True, 'align': 'center'})
    #     txt = workbook.add_format({'font_size': '13px', 'align': 'center', 'border':1})
    #     sheet.merge_range('D7:J9', 'MACHINE TRANSFER REPORT', head)
    #
    #
    #     sheet.write(14,3, 'COMPANY NAME', txt)
    #     sheet.write(14,4, 'TRANSFER DATE', txt)
    #     sheet.write(14,5, 'TRANSFER', txt)
    #     sheet.write(14,6, 'CUSTOMER', txt)
    #     sheet.write(14,7, 'TRANSFER TYPE', txt)
    #     sheet.write(14,8, 'TRANSFER STATE', txt)
    #     sheet.write(14,9, 'MACHINE NAME', txt)
    #
    #
    #     print(data)
    #     row = 15
    #     for cust in docs:
    #         col = 3
    #         for i,j in cust.items():
    #             sheet.write(row, col, j, border)
    #             col+=1
    #         row+=1
    #
    #     workbook.close()
    #     output.seek(0)
    #     response.stream.write(output.read())
    #     output.close()





