from odoo import fields, models,api, tools, service
from odoo.addons.payment_custom import const
from odoo.addons.multisafepay_integration.controllers.main import MultisafeController
from odoo.tools import urls


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
        print("DEFAULT PAYMENT METHOD CODE")
        self.ensure_one()
        if self.code != 'multisafe':
            return super()._get_default_payment_method_codes()
        return const.DEFAULT_PAYMENT_METHOD_CODES


    def _multisafe_get_api_url(self):
        print("MULTISAFE API GET URL")
        self.ensure_one()
        # if self.state == 'enabled':
        #     return f'https://testapi.multisafepay.com/v1/json/orders?api_key={self.multisafe_api_key}'
        return f'https://testapi.multisafepay.com/v1/json/orders?api_key={self.multisafe_api_key}'



    def _build_request_url(self, endpoint, **kwargs):
        """Override of `payment` to build the request URL."""
        print("BUILD API REQUEST URL")
        print(endpoint, kwargs)
        if self.code != 'multisafe':
            return super()._build_request_url(endpoint, **kwargs)
        print(urls.urljoin(f'https://testapi.multisafepay.com/v1/json/orders?api_key={self.multisafe_api_key}', endpoint)
)
        return urls.urljoin(f'https://testapi.multisafepay.com/v1/json/orders?api_key={self.multisafe_api_key}', endpoint)



    def _build_request_headers(self, *args, **kwargs):
        """Override of `payment` to build the request headers."""
        print("BUILD REQUEST HEADER")
        print(args, kwargs)
        if self.code != 'multisafe':
            return super()._build_request_headers(*args, **kwargs)

        odoo_version = service.common.exp_version()['server_version']
        module_version = self.env.ref('base.module_multisafepay_integration').installed_version
        return {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.multisafe_api_key}',
            'Content-Type': 'application/json',
            'User-Agent': f'Odoo/{odoo_version} MollieNativeOdoo/{module_version}',
        }






