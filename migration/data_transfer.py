# -*- coding: utf-8 -*-

import xmlrpc.client

url_db1 = "http://localhost:8017"
db_1 = 'test177'
username_db_1 = '1'
password_db_1 = '1'
common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1), allow_none= True)
models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1), allow_none= True)



url_db2 = "http://localhost:8019"
db_2 = 'odoo_test_13'
username_db_2 = '1'
password_db_2 = '1'
common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2), allow_none= True)
models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2), allow_none= True)

uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})


purchase_order_v17 = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order', 'search_read', [[]],
                                         {'fields': ['id', 'name', 'partner_id','user_id', 'date_order','order_line', 'state'], 'order' : "id asc"})
purchase_order_line = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order.line', 'search_read',[[]])

contacts_v17 = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [[]], {'fields': ['id', 'name']})


product_product = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.product', 'search_read', [[]],
                                      {'order' : "id asc"})




for prod in product_product:

    new_pro = {
        "id" : prod.get('id'),
        'name': prod.get('name'),
        'list_price': prod.get('list_price'),
        'standard_price': prod.get('standard_price'),
        'type' : 'consu' if prod.get('detailed_type') == 'consu' else 'service',
        'default_code' : prod.get('default_code'),
        'image_1024': prod.get('image_1024'),
        'image_128': prod.get('image_128'),
        'image_1920': prod.get('image_1920'),
        'image_256': prod.get('image_256'),
        'image_512': prod.get('image_512'),


    }

    models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'create',[new_pro])


for contact in contacts_v17:
    new_contact = {
        'id' : contact.get('id'),
        'name' : contact.get('name')
    }

    models_2.execute_kw(db_2, uid_db2, password_db_2,'res.partner', 'create', [new_contact])



for order in purchase_order_v17:

    contact_name = order.get('partner_id')[1]
    new_purchase = {}
    contact = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'search', [[('name', '=', contact_name)]])
    new_purchase = {
            'id' : order.get('id'),
            'name': order.get('name'),
            'partner_id': contact[0],
            'date_order': order.get('date_order'),
            'state': order.get('state')
        }
    models_2.execute_kw(
        db_2, uid_db2, password_db_2,
        'purchase.order', 'create',
        [new_purchase]
    )


for line in purchase_order_line:
    product_v17 = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.product', 'search_read', [[('id', '=' , line.get('product_id')[0])]], {'fields': ['id', 'name', 'default_code']})
    product_v19 = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'search_read', [[('default_code', '=', product_v17[0].get('default_code')),('name', 'like', product_v17[0].get('name'))]], {'fields': ['id', 'name']})
    if not product_v19:
        product_v19 = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'search_read', [[('name', '=', product_v17[0].get('name'))]], {'fields': ['id', 'name']})

    purchase_v17= models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order', 'search_read',[[('id', '=', line.get('order_id')[0])]],
                                      {'fields': ['id', 'name']})

    purchase_19= models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'search_read',[[('name', 'like', purchase_v17[0].get('name'))]],{'fields': ['id', 'name']})


    new_purchase_line = {
        'id' : line.get('id'),
        'name' : line.get('name'),
        'product_id' : product_v19[0].get('id'),
        'product_qty' : line.get('product_qty'),
        'price_unit' : line.get('price_unit'),
        'order_id' : purchase_19[0].get('id'),

    }
    models_2.execute_kw(db_2, uid_db2, password_db_2,'purchase.order.line', 'create', [new_purchase_line])

