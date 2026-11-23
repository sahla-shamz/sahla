# -*- coding: utf-8 -*-
{
    'name': 'Cyllo App Store (Client)',
    'version': '17.0.1.0.0',
    'category': 'Technical',
    'summary': 'Browse and install apps published on apps.cyllo.com from '
               'inside Cyllo ERP',
    'author': 'Cyllo',
    'company': 'Cyllo',
    'maintainer': 'Cyllo',
    'website': 'https://www.cyllo.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_config_parameter_data.xml',
        'views/cyllo_store_app_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'cyllo_store_client/static/src/js/search_panel_patch.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
