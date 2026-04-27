# -*- coding: utf-8 -*-

{
    "name" : "Customer Organization Chart",
    "version" : "19.0.1.0.0",
    "summary" : "Child Customer Organization chart ",
    "depends":[
        "base", "contacts"
    ],
    "data" : [
        "views/res_partner.xml"
    ],
    "installable" : True,
    "auto_install" : False,
    "application" : False,
    "assets" :{
            'web.assets_backend' : [
                "customer_org_chart/static/src/js/customer_org_chart.js",
                "customer_org_chart/static/src/xml/customer_org_chart.xml",
            ]
    }
}