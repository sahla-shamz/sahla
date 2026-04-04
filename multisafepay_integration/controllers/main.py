import http
from odoo.addons.payment.logging import get_payment_logger
import pprint

from odoo import http
from odoo.http import request

_logger = get_payment_logger(__name__)


class MultisafeController(http.Controller):
    _return_url = '/payment/multisafe/return'
    # _webhook_url = '/payment/razorpay/webhook'

    @http.route(_return_url, type='http', auth='public', methods=['POST'], csrf=False, save_session=False)
    def multisafe_return_from_checkout(self, **data):
        print("controller")
        _logger.info("Handling redirection from APS with data:\n%s", pprint.pformat(data))

        return request.redirect('/payment/status')