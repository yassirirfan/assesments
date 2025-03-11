# -*- coding: utf-8 -*-
import threading
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)


class PoSOrderWebhook(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create(self, vals):
        """
        Override create method to send a webhook asynchronously after PoS Order
        creation.

        Threading ensures that PoS orders are created quickly and reliably while
        sending webhooks asynchronously, avoiding performance issues,
        transaction rollbacks, and blocking delays.
        """
        record = super().create(vals)
        # Get webhook token before threading
        webhook_token = record.env['ir.config_parameter'].sudo().get_param(
            'webhook_exporter.webhook_token')
        if not webhook_token:
            _logger.error(
                "Webhook token is not configured in system parameters.")
            return record
        webhook_url = f'https://webhook.site/{webhook_token}'
        # Prepare data for webhook
        data = record.prepare_webhook_data()
        # Start thread to send webhook
        threading.Thread(target=record.send_webhook,
                         args=(webhook_url, data)).start()
        return record

    def prepare_webhook_data(self):
        """
        Prepares the data payload for the webhook.
        """
        return {
            'pos_order_id': self.id,
            'name': self.name,
            'date_order': str(self.date_order),
            'state': self.state,
            'amount_total': self.amount_total,
            'amount_tax': self.amount_tax,
            'amount_paid': self.amount_paid,
            'amount_return': self.amount_return,
            'customer': {
                'id': self.partner_id.id if self.partner_id else None,
                'name': self.partner_id.name if self.partner_id else None,
                'email': self.partner_id.email if self.partner_id else None,
                'phone': self.partner_id.phone if self.partner_id else None,
                'city': self.partner_id.city if self.partner_id else None,
                'zip': self.partner_id.zip if self.partner_id else None,
                'country_name': self.partner_id.country_id.name if self.partner_id and self.partner_id.country_id else None,
            },
            'session': {
                'id': self.session_id.id,
                'name': self.session_id.name,
                'config_id': self.session_id.config_id.id,
                'config_name': self.session_id.config_id.name,
            },
            'lines': [
                {
                    'id': line.id,
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'product_default_code': line.product_id.default_code,
                    'qty': line.qty,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                    'price_subtotal_incl': line.price_subtotal_incl,
                    'discount': line.discount,
                    'tax_ids': [(tax.id, tax.name) for tax in line.tax_ids],
                }
                for line in self.lines
            ],
            'payments': [
                {
                    'id': payment.id,
                    'name': payment.payment_method_id.name,
                    'amount': payment.amount,
                    'currency': payment.currency_id.name
                }
                for payment in (self.payment_ids or [])
            ],
            'company': {
                'id': self.company_id.id,
                'name': self.company_id.name,
            },
            'user': {
                'id': self.user_id.id,
                'name': self.user_id.name,
            },
            'pricelist': {
                'id': self.pricelist_id.id,
                'name': self.pricelist_id.name,
            },
            'fiscal_position': {
                'id': self.fiscal_position_id.id if self.fiscal_position_id else None,
                'name': self.fiscal_position_id.name if self.fiscal_position_id else None,
            },
            'note': getattr(self, 'general_note', None),
        }

    @staticmethod
    def send_webhook(webhook_url, data):
        """
        Sends the webhook request in a separate thread.
        """
        import requests  # Import inside the method to avoid threading issues
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(webhook_url, json=data, headers=headers)
            response.raise_for_status()
            _logger.info(
                f"Webhook sent successfully to {webhook_url}. Response: {response.text}")
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error sending webhook to {webhook_url}: {e}")
