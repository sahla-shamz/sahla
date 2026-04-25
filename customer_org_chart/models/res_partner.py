from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    parent_partner_id = fields.Many2one("res.partner", string="Parent Contact", domain=[("is_child", "=", False)])
    is_child= fields.Boolean(string="Is Child", default=False, compute="_compute_is_child", store=True)
    is_parent = fields.Boolean(string="Is Parent", default=False, store=True, compute="_compute_is_parent")
    customer_child_ids = fields.One2many("res.partner", "parent_partner_id", string="Child Contacts")

    @api.depends("parent_partner_id")
    def _compute_is_child(self):
        for rec in self:
            if rec.parent_partner_id:
                rec.is_child = True
            else:
                rec.is_child = False


    @api.depends("parent_partner_id")
    def _compute_is_parent(self):
        for rec in self:
            if rec.parent_partner_id:
                rec.parent_partner_id.is_parent = True
            else:
                rec.is_parent = False





    # def get_contact_hierarchy(self):
    #     print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    #     hierarchy = {
    #         'parent': {
    #             'id': self.parent_partner_id.id,
    #             'name': self.parent_partner_id.name,
    #         } if self.parent_partner_id else False,
    #         'self': {
    #             'id': self.id,
    #             'name': self.name,
    #         },
    #         'children': [
    #             {
    #                 'id': child.id,
    #                 'name': child.name,
    #             } for child in self.customer_child_ids
    #         ]
    #     }
    #
    #     return hierarchy