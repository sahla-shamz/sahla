# -*- coding: utf-8 -*-

from odoo import models, api

class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def get_location_details(self):
        """To get the company state through orm call"""
        state = self.env.company.state_id.name
        return state