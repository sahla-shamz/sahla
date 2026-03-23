from odoo import api, fields, models
import io
import xlsxwriter

class MachineTransferReport(models.AbstractModel):
    _name = "machine.transfer.report"
    _description = "Machine Transfer Report"


    def get_xlsx_report(self, data, response):
        print("getting xlsx report")
        docs=data
        print(docs)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        border = workbook.add_format({'border': 1})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '23px', 'valign' : 'vcenter'})
        unique = workbook.add_format(
            {'bold': True, 'font_size': '15px','valign': 'vcenter', 'align': 'center'})
        txt = workbook.add_format({'font_size': '13px',
                                   'align': 'center',
                                   'border': 1, 'pattern': 1,
                                   'bg_color': '#AAAAAA', 'valign': 'vcenter'})

        sheet.merge_range('B4:H6', 'MACHINE TRANSFER REPORT', head)

        unique_cust = len(set([dict['name'] for dict in docs])) == 1
        print(unique_cust,"unique customer")

        unique_machine = len(set([dict['machine_name'] for dict in docs])) == 1
        print(unique_machine, "unique machine")


        sheet.set_column(1, 8, 24)
        sheet.set_row(14, 30)
        install=[]
        remove=[]
        for dict in docs:
            if dict['transfer_type'] == 'install':
                install.append(dict)
            elif dict['transfer_type'] == 'remove':
                remove.append(dict)

        row = 14
        col = 1

        if install:
            sheet.write(row, col, 'TRANSFER', txt)
            col += 1
            if not unique_machine:
                sheet.write(row, col, 'MACHINE NAME', txt)
                col += 1
            if not unique_cust:
                sheet.write(row, col, 'CUSTOMER', txt)
                col += 1
            sheet.write(row, col, 'TRANSFER DATE', txt)
            col += 1
            sheet.write(row, col, 'TRANSFER TYPE', txt)
            col += 1
            sheet.write(row, col, 'TRANSFER STATE', txt)
            col += 1
            sheet.write(row, col, 'COMPANY NAME', txt)

            row = 15
            for dict in install:
                col = 1
                for key, val in dict.items():
                    if unique_cust and key == 'name' or unique_machine and key == 'machine_name':
                        continue
                    if key == 'machine_name' or key == 'transfer_type' or key == 'transfer_states':
                        dict[key] = val.capitalize()
                        sheet.write(row, col, dict[key], border)
                        col += 1
                    else:
                        sheet.write(row, col, val, border)
                        col += 1
                row += 1

        print(row, "row")
        print(col, "col")
        print(remove)

        if remove:
            col=1
            if install:
                row+=2
            sheet.write(row, col, 'TRANSFER', txt)
            col += 1
            sheet.write(row, col, 'MACHINE NAME', txt)
            col += 1
            sheet.write(row, col, 'TRANSFER DATE', txt)
            col += 1
            sheet.write(row, col, 'TRANSFER TYPE', txt)
            col += 1
            sheet.write(row, col, 'TRANSFER STATE', txt)
            col += 1
            sheet.write(row, col, 'COMPANY NAME', txt)

            row+=1
            for dict in remove:
                col = 1
                for key, val in dict.items():
                    if key == 'name':
                        continue
                    if key == 'machine_name' or key == 'transfer_type' or key == 'transfer_states':
                        dict[key] = val.capitalize()
                        sheet.write(row, col, dict[key], border)
                        col += 1
                    else:
                        sheet.write(row, col, val, border)
                        col += 1
                row += 1

        if unique_cust and not remove:
            sheet.merge_range('B11:C12', f'Customer :{dict['name']}', unique)


        if unique_machine:
            sheet.merge_range('B9:C10', f'Machine :{dict['machine_name']}', unique)


        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
