from odoo import fields, models,api
from odoo.addons.payment_custom import const


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



    # def _multisafe_get_api_url(self):
    #     """ Return the API URL according to the state.
    #
    #     Note: self.ensure_one()
    #
    #     :return: The API URL
    #     :rtype: str
    #     """
    #     self.ensure_one()
    #     if self.state == 'enabled':
    #         return 'https://testapi.multisafepay.com/v1/json/orders'
