# -*- coding: utf-8 -*-

from odoo import fields, models, api

class DataSearch(models.TransientModel):
    _name = "data.search"
    _description = "Data Search"

    model_id= fields.Many2one("ir.model", string="Model")
    field_id = fields.Many2one("ir.model.fields",string="Field Name")
    search_rec = fields.Char(string="Search Content")
    search_date = fields.Datetime("Search Date")
    is_date = fields.Boolean("Is Date Field", default=False, compute="_compute_is_date")
    one2many_field_id= fields.Many2one("ir.model.fields",string="One2many Field")
    one2many_model= fields.Integer("one2many", compute="_compute_one2many_model")
    is_one2many= fields.Boolean("Is One2many", default=False, compute="_compute_is_one2many")
    search_boolean = fields.Selection([('true', 'True'), ('false', 'False')], string="Search Boolean")
    is_boolean =  fields.Boolean("Is Boolean Field", default=False, compute="_compute_is_boolean")
    field_ids= fields.Many2many('ir.model.fields', string="Fields", compute="_compute_field_ids")
    selection_ids= fields.Many2one("ir.model.fields.selection", string="Selection Fields")
    is_selection= fields.Boolean("Is Selection Field", default=False, compute="_compute_is_selection")

    @api.depends('field_id')
    def _compute_is_date(self):
        """Check whether the field type is date"""
        for rec in self:
            if self.field_id.ttype in ['date', 'datetime']:
                rec.is_date = True
            else:
                rec.is_date = False


    @api.depends("field_id")
    def _compute_one2many_model(self):
        """Get the related modal name if the field type is One2Many"""
        for rec in self:
            related_model= self.field_id.relation
            model= self.env['ir.model'].search([]).filtered(lambda l : l.model == related_model)
            rec.one2many_model = model.id



    @api.depends('field_id')
    def _compute_is_one2many(self):
        """Check whether the field type is one2many"""
        for rec in self:
            if rec.field_id.ttype == 'one2many' :
                rec.is_one2many = True
            else:
                rec.is_one2many = False



    @api.depends('field_id')
    def _compute_is_boolean(self):
        for rec in self:
            if rec.field_id.ttype == 'boolean':
                rec.is_boolean = True
            else:
                rec.is_boolean = False

    @api.depends('field_id')
    def _compute_is_selection(self):
       for rec in self:
           print("helooo")
           if self.field_id.ttype == 'selection':
               rec.is_selection = True
           else:
               rec.is_selection = False


    def action_search(self):
        """Get the records based on the field type and display warning if any
            field is empty or the there are no records found"""
        if self.field_id.ttype in ['date', 'datetime']:
            records = self.env[self.model_id.model].search([(self.field_id.name, '=', self.search_date)])

        elif self.field_id.ttype == 'one2many':
            if not self.one2many_field_id:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'danger',
                        'message': "Set the One2Many field",
                    }
                }
            field= self.field_id.name + "." + self.one2many_field_id.name
            records= self.env[self.model_id.model].search([(field, 'ilike', self.search_rec)])



        elif self.field_id.ttype == 'boolean' :
            print("booolllean")
            print(self.search_boolean)
            if not self.search_boolean:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'danger',
                        'message': "Select True or False to search",
                    }
                }
            if self.search_boolean == 'true':
                records = self.env[self.model_id.model].search([(self.field_id.name, '=', True)])
            else:
                records = self.env[self.model_id.model].search([(self.field_id.name, '=', False)])


        elif self.field_id.ttype == 'selection' :
            print("selection")
            print(self.field_id.selection_ids)
            if not self.selection_ids:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'danger',
                        'message': "Select a selection field to search",
                    }
                }
            records = self.env[self.model_id.model].search([(self.field_id.name, '=', self.selection_ids.value)])



        else:
            if not self.model_id or not self.field_id:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'danger',
                        'message': "Set the Model and field to search",
                    }
                }
            records = self.env[self.model_id.model].search([(self.field_id.name, 'ilike', self.search_rec)])

        if not records:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'danger',
                    'title': 'No record Found!',
                    'message': "Try another model or field",
                }
            }

        return{
            "name" : self.model_id.name,
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model" : self.model_id.model,
            "domain": [('id', 'in', records.ids)],
        }

    @api.depends('model_id')
    def _compute_field_ids(self):
        for rec in self:
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # print(self.model_id.search([('id', 'in', rec.model_id)]))
            idss= self.field_id.search([]).filtered(lambda l : l.store == False and l.ttype == 'boolean' and l.model_id == rec.model_id)
            print(idss)
            print(len(idss))
            rec.field_ids = [fields.Command.set(idss.ids)]
            # rec.field_ids = idss
            print(rec.field_ids)


