import http

import requests

class MultisafeController(http.Controller):
    _return_url = '/payment/multisafe/return'
    # _webhook_url = '/payment/razorpay/webhook'

    @http.route(
        _return_url,
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False,
        save_session=False,
    )
    def multisafe_pay_process(self, reference, **data):
        """Process the payment data sent by Razorpay after redirection from checkout."""

        url = "https://testapi.multisafepay.com/v1/json/orders?api_key=9286447de823d2102314cb3abe2a2c2e417f0ba1"

        payload = {
            "payment_options": { "close_window": False },
            "customer": {
                "locale": "en_US",
                "disable_send_email": False
            },
            "checkout_options": { "validate_cart": False },
            "days_active": 30,
            "seconds_active": 2592000,
            "order_id": "test_order_0001",
            "currency": "EUR",
            "amount": 1000,
            "description": "Test order description"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.text)
