{
    "name" : "POS Sale Order",
    "summary" : "POS Sale Order",
    "version": "19.0.1.0.0",
    "depends" : [
        "base","point_of_sale", "pos_sale"
    ],
    "data" : [
        "views/pos_conf.xml"
    ],
    "assets": {
        'point_of_sale._assets_pos': [

            "pos_sale_order/static/src/app/components/infopopup.js",
            "pos_sale_order/static/src/js/control_button.js",
            "pos_sale_order/static/src/app/components/infopopup.xml",
            "pos_sale_order/static/src/xml/control_button_inherit.xml",

        ]
    }

}