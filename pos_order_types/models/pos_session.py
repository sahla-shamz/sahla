from odoo import api, fields, models

class PosSession(models.Model):
    _inherit = 'pos.session'


    @api.model
    def _load_pos_data_models(self, config):
        models = super()._load_pos_data_models(config)
        models += ['pos.order.type']
        return models
