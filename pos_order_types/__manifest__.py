# -*- coding: utf-8 -*-

{
    "name" : "POS Order Types",
    "version" : "19.0.1.0.0",
    "depends": [
        "point_of_sale", "base"
    ],
    "data" : [
        "security/ir.model.access.csv",
        "data/order_type_data.xml",
        "views/pos_conf.xml"
    ],
    "assets": {
        'point_of_sale._assets_pos': [
            "pos_order_types/static/src/js/control_button.js",
            "pos_order_types/static/src/xml/control_button_inherit.xml",
            "pos_order_types/static/src/xml/order_reciept_inherit.xml"

        ]
    },
    "installable": True,
    "auto_install": False,
    "application" : False
}