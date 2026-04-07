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


from odoo.addons.multisafepay_integration.controllers.main import MultisafeController

_logger = get_payment_logger(__name__)


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"


    def _get_specific_rendering_values(self,processing_values):
        print("GET SPECIFIC RENDERING VALUES")
        print(processing_values)
        if self.provider_code != 'multisafe':
            return super()._get_specific_rendering_values(processing_values)
        base_url = self.provider_id.get_base_url()
        api_url= self.provider_id._multisafe_get_api_url()

        payload = {
            "customer": {
                "locale": "en_US",
                "disable_send_email": False,
                "first_name": self.env.user.name,
                "country": self.env.user.country_id.name,
                "email": self.env.user.email,
            },
            "checkout_options": {"validate_cart": True},
            "days_active": 30,
            "seconds_active": 2592000,
            "order_id": self.reference,
            "currency": self.currency_id.name,
            "amount": self.amount *100,
            "type" : "redirect",
            "description": "Test order description",

            "payment_options": {
                "redirect_url": url_join(base_url, "/payment/multisafe/return"),
                "notification_url": url_join(base_url ,"/payment/multisafe/webhook"),
                "notification_method": "POST",
                'return_url': url_join(base_url, "/payment/multisafe/return"),
                "cancel_url": url_join(base_url, "/payment/multisafe/return")
            },

        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }


        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        data = response.json()
        payload.update({
            'payment_url' : data.get('data').get('payment_url')
        })


        payment_data = response.json()
        self.provider_reference = payment_data.get('data').get('order_id')
        checkout_url = payload['payment_url']
        parsed_url = url_parse(checkout_url)
        url_params = url_decode(parsed_url.query)
        return {'api_url': checkout_url,
                'url_params': url_params, }



    def _apply_updates(self, payment_data):
        """Override of `payment` to update the transaction based on the payment data."""
        print("APPLY UPDATES")
        print(payment_data)
        if self.provider_code != 'multisafe':
            return super()._apply_updates(payment_data)

        # Update the payment method.
        # print("self", self)
        self.payment_method_id = self.payment_method_id

        # Update the payment state.
        payment_status = payment_data.get('data').get('payment_methods')[0].get('status')
        if payment_status in ('initialized', 'open'):
            self._set_pending()
        elif payment_status == 'authorized':
            self._set_authorized()
        elif payment_status == 'completed':
            self._set_done()
        elif payment_status in ['declined', 'uncleared', 'cancelled']:
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
        print("EXTRACT REFERENCE")
        print(payment_data)
        if provider_code != 'multisafe':
            return super()._extract_reference(provider_code, payment_data)
        return payment_data.get('transactionid')



    @staticmethod
    def _verify_and_process(data):
        print("VERIFY AND PROCESS")
        print("data")
        tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference('multisafe', data)
        # print("tx_sudo", tx_sudo)
        if not tx_sudo:
            return

        try:
            verified_data = tx_sudo._send_api_request(
                'GET', f'/{tx_sudo.provider_reference}'
            )

        except ValidationError:
            _logger.error("Unable to process the payment data")
        else:
            tx_sudo._process('multisafe', verified_data)




    def _extract_amount_data(self, payment_data):
        """Override of `payment` to extract the amount and currency from the payment data."""
        print("EXTRACT AMOUNT DATA")
        print(payment_data)
        if self.provider_code != 'multisafe':
            return super()._extract_amount_data(payment_data)

        # print(payment_data)
        amount_data = payment_data.get('data', {})
        # print("amount data", amount_data)
        amount = amount_data.get('amount') / 100
        currency_code = amount_data.get('currency')
        # print(amount, currency_code)
        return {
            'amount': float(amount),
            'currency_code': currency_code,
        }

