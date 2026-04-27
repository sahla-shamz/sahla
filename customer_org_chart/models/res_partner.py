# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    parent_partner_id = fields.Many2one("res.partner", string="Parent Contact", domain=[("is_child", "=", False)])
    is_child= fields.Boolean(string="Is Child", default=False, compute="_compute_is_child", store=True)
    is_parent = fields.Boolean(string="Is Parent", default=False, store=True, compute="_compute_is_parent")
    customer_child_ids = fields.One2many("res.partner", "parent_partner_id", string="Child Contacts")

    @api.depends("parent_partner_id")
    def _compute_is_child(self):
        """Compute whether the partner is a child customer or not"""
        for rec in self:
            if rec.parent_partner_id:
                rec.is_child = True
            else:
                rec.is_child = False


    @api.depends("parent_partner_id")
    def _compute_is_parent(self):
        """Compute whether the partner is a parent customer or not"""
        for rec in self:
            if rec.parent_partner_id:
                rec.parent_partner_id.is_parent = True
            else:
                rec.is_parent = False

