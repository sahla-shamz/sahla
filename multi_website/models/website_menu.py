# -*- coding: utf-8 -*-

from odoo import fields, models


class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    active = fields.Boolean(default=True, string="Active")
