# -*- coding: utf-8 -*-
from random import randint

from odoo import fields,models

class MachineTags(models.Model):
    _name = 'machine.tags'
    _description = 'Machine Tags'
    _rec_name = "tag"

    tag=fields.Char(string='Tag')
    color = fields.Integer('Color')

