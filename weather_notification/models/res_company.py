from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = "res.company"



    @api.model
    def get_location_details(self):
        state = self.env.company.state_id.name
        print(state)
        return state