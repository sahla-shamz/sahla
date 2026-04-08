# -*- coding: utf-8 -*-

{
    "name": "Multisafe Pay Payment Provider",
    "summary": "Multisafe Pay Payment Provider",
    "version": "19.0.1.0.0",
    "depends" : [
        "base", "payment"
    ],
    "data" : [
        "views/redirect_template.xml",
        "data/payment_method_data.xml",
        "data/payment_provider_data.xml",
        "views/payment_provider_views.xml",
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    "installable" : True,
    "auto_install" : False,
    "application" : True,
}