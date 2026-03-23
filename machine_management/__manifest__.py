# -*- coding: utf-8 -*-

{
    "name": "Machine Management",
    "description": "Machine Mangement App",
    "application": True,
    'category' : 'Website',
    "depends": ["base","mail","product","sale", "account", "website", 'web', "website_sale"],
    'data':['security/machine_security.xml',
            'security/ir.model.access.csv',
            'data/machine_type_data.xml',
            'data/sequence_machine.xml',
            'data/machine_tags_data.xml',
            'data/new_product_data.xml',
            'data/mail_template.xml',
            'data/ir_cron_data.xml',
            'report/transfer_report.xml',
            'report/machine_transfer_reports.xml',
            'wizard/machine_transfer_reporting.xml',
            'views/snippets/machine_template_highlights.xml',
            'views/website_cart.xml',
            'views/website_machines.xml',
            'views/website_create_customer.xml',
            'views/website_machine_service.xml',
            'views/machine_management.xml',
            'views/machine_management_menu.xml',

            ],
    'assets': {
        'web.assets_backend': [
            'machine_management/static/src/js/action_manager.js',

        ],
        'web.assets_frontend': [
            'machine_management/static/src/xml/machine_highlight_content.xml',
            'machine_management/static/src/js/machine_highlight.js',
        ]
    }
}