import http
from odoo.addons.payment.logging import get_payment_logger
import pprint

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = get_payment_logger(__name__)


class MultisafeController(http.Controller):
    # _return_url = 'https://testpayv2.multisafepay.com/connect/823PXT7DY66GxIREm3G13PNvAB0LTRYDFju/?lang=en_US'
    _return_url = '/payment/multisafe/return'
    _webhook_url = '/payment/multisafe/webhook'

    @http.route(_return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False, save_session=False)
    def multisafe_return_from_checkout(self, **data):
        print("controller")
        print("controller data", data)
        _logger.info("Handling redirection from APS with data:\n%s", pprint.pformat(data))
        self._verify_and_process(data)
        return request.redirect('/payment/status')
        # tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference('multisafe', data)
        # print("tx_sudo", tx_sudo)
        # if tx_sudo:
        #     self._verify_signature(data, tx_sudo)
        #     tx_sudo._process('multisafe', data)
        # return request.redirect('/payment/status')

    @http.route(_webhook_url, type='http', auth='public', methods=['POST'], csrf=False)
    def multisafe_webhook(self, **data):
        _logger.info("notification received from Multisafe with data:\n%s", pprint.pformat(data))
        print("webbbhooook")
        self._verify_and_process(data)
        return ''  # Acknowledge the notification

    @staticmethod
    def _verify_and_process(data):
        print("verifying data")
        tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference('multisafe', data)
        print("tx_sudo", tx_sudo)
        if not tx_sudo:
            return

        try:
            verified_data = tx_sudo._send_api_request(
                'GET', f'/payments/{tx_sudo.provider_reference}'
            )
        except ValidationError:
            _logger.error("Unable to process the payment data")
        else:
            tx_sudo._process('multisafe', verified_data)
