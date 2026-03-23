from odoo import http
from odoo.http import request


class WebsiteClearCart(http.Controller):
    @http.route(['/shop/cart/clear'], type='http', auth="public", website=True)


    def _get_current_lines(self):
        """Delete the current sale order when clicking the 'Clear Cart Button' """
        current= request.cart
        current.unlink()

        return request.redirect('/shop/cart/')



