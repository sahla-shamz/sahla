{
    "name" : "Website Product Visibility",
    "description" : "Website Product Visibility",
    "version" : "19.0.1.0.0",
    "category" : "website",
    "depends": ["product", "sale", "website_sale", "portal"],
    "data": [
        "views/res_partner.xml",
        "views/portal_template.xml",
        "views/product_portal_template.xml",
        "views/product_template.xml"
    ],
    "installable" : True,
    "auto_install" : False,
    "application" : False,
}