# -*- coding: utf-8 -*-

from odoo.addons.payment.logging import get_payment_logger
import pprint
from odoo import http
from odoo.http import request

_logger = get_payment_logger(__name__)


class MultisafeController(http.Controller):
    _return_url = '/payment/multisafe/return'
    _webhook_url = '/payment/multisafe/webhook'

    @http.route(_return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False, save_session=False)
    def multisafe_return_from_checkout(self, **data):
        """Redirect to success page after successful payment"""
        _logger.info("Handling redirection from APS with data:\n%s", pprint.pformat(data))
        tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference('multisafe', data)
        if tx_sudo:
            tx_sudo._verify_and_process(data)
        return request.redirect('/payment/status')

    @http.route(_webhook_url, type='http', auth='public', methods=['POST'], csrf=False)
    def multisafe_webhook(self, **data):
        """Redirect to recieve the notification with webhook url"""
        _logger.info("notification received from Multisafe with data:\n%s", pprint.pformat(data))
        data = request.get_json_data()
        self._verify_and_process(data)
        return ''

