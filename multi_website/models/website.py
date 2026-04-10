# -*- coding: utf-8 -*-

from odoo import fields, models

class Website(models.Model):
    _inherit = "website"


    active = fields.Boolean(default=True, string="Active")



    def action_archive(self):
        """
        Archive the website also changes the id of the records linked to website with new website
        """
        main_website = self.search([], order= "id desc", limit=1)
        print(main_website)
        for record in self:
            sale_orders= self.env['sale.order'].search([('website_id', '=', record.id)])
            print(sale_orders)

            for rec in sale_orders:
                print(rec.invoice_ids.website_id)
                rec.write({'website_id': main_website.id,
                           })

                rec.invoice_ids.write({
                    'website_id': main_website.id,
                })

            pricelists= self.env['product.pricelist'].search([])

            for pricelist in pricelists:
                if pricelist.website_id:

                    pricelist.write({
                        'website_id': main_website.id,
                    })


            self.env.company.write({'website_id': main_website.id})

            # print(self.env.user.website_id)

            self.env['website.menu'].search([('website_id', '=', record.id), ('website_id', '!=', False)]).action_archive()

            [product.write({'website_id' : main_website.id}) for product in self.env['product.wishlist'].search([])]
                
        return super().action_archive()



    def action_unarchive(self):
        """
        Unarchiving websites also unarchives the menus
        """

        for rec in self:
            print(self.env['website.menu'].search([('website_id', '=', rec.id), ('active', '=', False)]))

            self.env['website.menu'].search(
                [('website_id', '=', rec.id), ('active', '=', False)]).action_unarchive()
            
        return super().action_unarchive()

