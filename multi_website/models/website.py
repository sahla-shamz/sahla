# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import UserError


class Website(models.Model):
    _inherit = "website"

    active = fields.Boolean(default=True, string="Active")

    def action_archive(self):
        """
        Archive the website also changes the id of the related records with new website
        """
        main_website = self.search([], order= "id desc", limit=1)
        for record in self:
            if main_website == record:
                raise UserError("Cannot archive newly created website. Try archiving the other websites.")
            self.env['website.menu'].search(
                [('website_id', '=', record.id), ('website_id', '!=', False)]).action_archive()
            models = (self.env['ir.model.fields'].search([("name", "=", "website_id")]).model_id.
                      filtered(lambda l: not l.abstract and not l.transient and
                                         l.model != 'sale.report' and l.model != 'website.menu'))

            for model in models:
                for rec in self.env[model.model].sudo().search([('website_id', '=', record.id)]):
                    if self.env[model.model].fields_get(allfields=['company_id']):
                        if self.env.company.id == rec.company_id.id or not rec.company_id:
                            rec.write({"website_id": main_website.id})
                    else:
                        rec.write({"website_id": main_website.id})

        return super().action_archive()



    def action_unarchive(self):
        """
        Unarchiving websites also unarchives the menus
        """
        for rec in self:
            self.env['website.menu'].search(
                [('website_id', '=', rec.id), ('active', '=', False)]).action_unarchive()
            
        return super().action_unarchive()

