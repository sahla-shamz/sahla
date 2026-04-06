from odoo.addons.payment.logging import get_payment_logger
from odoo import api, fields, models, release, _
import requests
from werkzeug.urls import url_decode, url_parse
from odoo.exceptions import ValidationError
from odoo.tools import urls
from odoo.tools.urls import urljoin as url_join
from odoo.http import Controller, request, Response, route
from odoo.addons.payment import utils as payment_utils
import json
# from odoo.addons.multisafepay_integration import const


from odoo.addons.multisafepay_integration.controllers.main import MultisafeController

_logger = get_payment_logger(__name__)


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"


    def _get_specific_rendering_values(self,processing_values):
        if self.provider_code != 'multisafe':
            return super()._get_specific_rendering_values(processing_values)
        base_url = self.provider_id.get_base_url()
        api_url= self.provider_id._multisafe_get_api_url()
        return_url= url_join(base_url, "/payment/multisafe/return")
        # redirect_url = url_join(base_url, "/payment/status"),
        # webhook_url = url_join(base_url, "/payment/multisafe/webhook"),
        redirect_url = urls.urljoin(base_url, MultisafeController._return_url)
        webhook_url = urls.urljoin(base_url, MultisafeController._webhook_url)

        payload = {
            "customer": {
                "locale": "en_US",
                "disable_send_email": False,
                "first_name": "John",
                "last_name": "Doe",
                "country": "US",
                "email": "abc@gmail.com",
            },
            "checkout_options": {"validate_cart": True},
            "days_active": 30,
            "seconds_active": 2592000,
            "order_id": self.reference,
            "currency": self.currency_id.name,
            "amount": self.amount,
            "type" : "redirect",
            "transaction_id": self.id,
            "description": "Test order description",
            'return_url': url_join(base_url ,"/payment/multisafe/return"),
            # 'redirectUrl': f'{redirect_url}?ref={self.reference}',
            'webhookUrl': f'{webhook_url}?ref={self.reference}',
            # 'return_url': url_join(base_url ,"/payment/multisafe/return"),
            "redirect_url": url_join(base_url ,"/payment/status"),
            "payment_options": {
                # "redirect_url": "/payment/status",
                "notification_url": "https://www.example.com/paymentnotification",
                "notification_method": "POST",
                "redirect_url": url_join(base_url, "/payment/status"),
                'return_url': url_join(base_url, "/payment/multisafe/return")
            },

        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        # response = requests.post(api_url, json=payload, headers=headers)
        # print(response.text)

            # payment_url = item.get('data').get('payment_url')
        # print(payment_url)
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        data = response.json()
        # print(data.get('data').get('payment_url'))
        payload.update({
            'payment_url' : data.get('data').get('payment_url')
        })

        print(payload)

        # try:
        #     payment_data = self._send_api_request('POST', '/payments', json=payload)
        # except ValidationError as error:
        #     self._set_error(str(error))
        #     return {}
        payment_data = self._send_api_request('POST', f'/', json=payload)
        print("paymennttt", payment_data)
        payment_data = response.json()
        self.provider_reference = payment_data.get('data').get('order_id')
        print("ref", self.provider_reference)
        checkout_url = payload['payment_url']
        parsed_url = url_parse(checkout_url)
        url_params = url_decode(parsed_url.query)
        return {'api_url': checkout_url, 'url_params': url_params, 'redirect_url' : redirect_url,
                'return_url' : return_url, 'payload' : payload}



    def _apply_updates(self, payment_data):
        """Override of `payment` to update the transaction based on the payment data."""
        print("Hellooo")
        if self.provider_code != 'multisafe':
            return super()._apply_updates(payment_data)

        # Update the payment method.
        payment_method_type = payment_data.get('method', '')
        if payment_method_type == 'creditcard':
            payment_method_type = payment_data.get('details', {}).get('cardLabel', '').lower()
        # payment_method = self.env['payment.method']._get_from_code(
        #     payment_method_type, mapping=const.PAYMENT_METHODS_MAPPING
        # )
        # self.payment_method_id = payment_method or self.payment_method_id

        # Update the payment state.
        payment_status = payment_data.get('status')
        if payment_status in ('pending', 'open'):
            self._set_pending()
        elif payment_status == 'authorized':
            self._set_authorized()
        elif payment_status == 'paid':
            self._set_done()
        elif payment_status in ['expired', 'canceled', 'failed']:
            self._set_canceled(_("Cancelled payment with status: %s", payment_status))
        else:
            _logger.info(
                "Received data with invalid payment status (%s) for transaction %s.",
                payment_status, self.reference
            )
            self._set_error(_("Received data with invalid payment status: %s.", payment_status))


    @api.model
    def _extract_reference(self, provider_code, payment_data):
        """Override of `payment` to extract the reference from the payment data."""
        print("extract reference")
        if provider_code != 'multisafe':
            return super()._extract_reference(provider_code, payment_data)
        # print(self.payload, "payloaaaaaaaaaaadddd")
        return payment_data.get('ref')



