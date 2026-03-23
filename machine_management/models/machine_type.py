# -*- coding: utf-8 -*-

from odoo import api, fields, models

class MachineType(models.Model):
    _name = 'machine.type'
    _description = 'Machine Type'
    _rec_name = 'machine_type'
    _inherit = ['mail.thread']

    machine_type=fields.Char(string='Machine Type', required=True)