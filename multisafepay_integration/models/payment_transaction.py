from odoo import api, fields, models, release
import requests
from odoo.tools import urls
from odoo.tools.urls import urljoin as url_join
from odoo.http import Controller, request, Response, route
from odoo.addons.payment import utils as payment_utils


from odoo.addons.multisafepay_integration.controllers.main import MultisafeController

class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _get_specific_rendering_values(self,processing_values):
        if self.provider_code != 'multisafe':
            return super()._get_specific_rendering_values(processing_values)
        base_url = self.provider_id.get_base_url()
        api_url= self.provider_id._multisafe_get_api_url()
        payload = {
            'api_url': self.provider_id._multisafe_get_api_url()+f"{self.id}",
            "customer": {
                "locale": "en_US",
                "disable_send_email": False
            },
            "checkout_options": {"validate_cart": False},
            "days_active": 30,
            "seconds_active": 2592000,
            "order_id": self.reference,
            "currency": self.currency_id.name,
            "amount": self.amount,
            # "type" : "redirect",
            "transaction_id": self.id,
            "description": "Test order description",
            'return_url': url_join(base_url ,"/payment/multisafe/return"),
            "redirect_url": url_join(base_url ,"/payment/status"),
            "payment_options": {
                "redirect_url": "/payment/status",
            }
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(api_url, json=payload, headers=headers)
        # print(response.text.split(",")[3])
        print(response.text)
        print(payload)
        return payload


