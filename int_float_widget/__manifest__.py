# -*- coding: utf-8 -*-

{
    "name": "Int Float Widget",
    "version": "19.0.1.0.0",
    "summary": "Int Float Widget",

    "data" : [
        "views/res_partner.xml"
    ],
    "assets" :{
        'web.assets_backend' : [
            "int_float_widget/static/src/xml/float_int.xml",
            "int_float_widget/static/src/js/float_int.js",
        ]

    },
    "installable": True,
    "auto_install": False,
    "application": False,
}