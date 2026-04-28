from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_order_type_id = fields.Many2many("pos.order.type",related="pos_config_id.order_type_id",readonly=False)
    pos_is_enable_order_type = fields.Boolean(related="pos_config_id.is_enable_order_type",readonly=False)