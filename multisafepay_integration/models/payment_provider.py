from odoo import fields, models,api, tools
from odoo.addons.payment_custom import const
from odoo.addons.multisafepay_integration.controllers.main import MultisafeController
from odoo.http import request


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('multisafe', 'MultiSafe')], ondelete={'multisafe': 'set default'})
    multisafe_api_key = fields.Char(
        string="API Key",
        help="The key solely used to identify the website with multisafe",
        required_if_provider='multisafe',
        copy=False,
    )


    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        self.ensure_one()
        if self.code != 'multisafe':
            return super()._get_default_payment_method_codes()
        return const.DEFAULT_PAYMENT_METHOD_CODES



    def _multisafe_get_api_url(self):
        self.ensure_one()
        if self.state == 'enabled':
            return f'https://testapi.multisafepay.com/v1/json/orders?api_key={self.multisafe_api_key}'




