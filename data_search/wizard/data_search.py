from odoo import fields, models, api
from odoo.exceptions import UserError


class DataSearch(models.Model):
    _name = "data.search"
    _description = "Data Search"


    field_id = fields.Many2one("ir.model.fields",string="Field Name")




    def action_search(self):
        print(self.field_id)
        print(self.env[self.field_id.model_id.model].search([]).mapped(self.field_id.name))
        records = self.env[self.field_id.model_id.model].sudo().search([]).mapped(self.field_id.name)

        if type(records) != list and records:
            return {

                "type": "ir.actions.act_window",
                "view_mode": "list,form",
                "res_model" : self.field_id.model_id.model,
                "target" : "new"

            }
        else:

            raise UserError("No records found")


