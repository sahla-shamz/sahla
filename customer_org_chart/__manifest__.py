{
    "name" : "Customer Organization Chart",
    "version" : "19.0.1.0.0",
    "summary" : "Child Customer Organization chart ",
    "description" : "",
    "depends":[
        "base", "hr_org_chart"
    ],
    "data" : [
        "views/res_partner.xml"
    ],
    "installable" : True,
    "auto_install" : False,
    "application" : False,
    "assets" :{
            'web.assets_backend' : [
                "customer_org_chart/static/src/xml/department_chart.xml",
                "customer_org_chart/static/src/js/department_chart.js",
            ]
    }
}