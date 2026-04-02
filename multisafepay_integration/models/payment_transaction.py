from odoo import api, fields, models
from odoo.tools import urls


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"


    def _get_specific_rendering_values(self, processing_values):

        if self.provider_code != 'multisafe':
            return super()._get_specific_rendering_values(processing_values)

        # return_url = urls.urljoin(self.provider_id.get_base_url(), BuckarooController._return_url)
        rendering_values = {
            'api_url': self.provider_id._multisafe_get_api_url(),
            'Brq_websitekey': self.provider_id.buckaroo_website_key,
            'Brq_amount': self.amount,
            'Brq_currency': self.currency_id.name,
            'Brq_invoicenumber': self.reference,
            # Include all 4 URL keys despite they share the same value as they are part of the sig.
            # 'Brq_return': return_url,
            # 'Brq_returncancel': return_url,
            # 'Brq_returnerror': return_url,
            # 'Brq_returnreject': return_url,
        }
        if self.partner_lang:
            rendering_values['Brq_culture'] = self.partner_lang.replace('_', '-')
        rendering_values['Brq_signature'] = self.provider_id._buckaroo_generate_digital_sign(
            rendering_values, incoming=False
        )
        return rendering_values
