# -*- coding: utf-8 -*-
{
    'name': 'Odoo Webhook Export',
    'version': '18.0.1.0.0',
    'summary': 'Automatically exports PoS order data to a webhook in JSON format.',
    'description': """
    This module extends the Point of Sale (PoS) functionality in Odoo by automatically 
    sending order data to a specified webhook URL in JSON format upon order creation.
    Perfect for integrating Odoo PoS with external systems, analytics tools, or third-party applications.
    """,
    'author': 'Yassir Irfan',
    'category': 'Tools',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'data/system_data.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
