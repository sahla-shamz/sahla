# -*- coding: utf-8 -*-

{
    "name" : "Sales Person Filter",
    "version" : "19.0.1.0.0",
    "description" : "select salesperson and filter the crm list view",
    "depends" : [
        "crm","web"
    ],
    "data" : [
        "views/salesperson_filter.xml"
    ],
    "assets" : {
        "web.assets_backend" : [
        "salesperson_filter/static/src/js/list_view_crm.js",
        "salesperson_filter/static/src/xml/list_view_crm.xml",
        ]
    },
    "installable" : True,
    "auto_install" : False,
    "application" : False,
}