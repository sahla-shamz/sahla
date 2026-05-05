import xmlrpc.client

url_db1 = "http://127.0.0.1:8017"
db_1 = 'test177'
username_db_1 = '1'
password_db_1 = '1'
common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1), allow_none=True)
models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1), allow_none=True)
version_db1 = common_1.version()



url_db2 = "http://localhost:8019"
db_2 = 'odoo_test_8'
username_db_2 = '1'
password_db_2 = '1'
common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2), allow_none=True)
models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2), allow_none=True)
version_db2 = common_2.version()

uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})


purchase_order_v17 = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order', 'search_read', [[]],
                                         {'fields': ['id', 'name', 'partner_id','user_id', 'date_order','order_line', 'state'], 'order' : "id asc"})
purchase_order_line = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order.line', 'search_read',[[]])
# print("PURCHASE ORDER LINES -------",purchase_order_line)

# new_lead = models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'create', [db_1_leads])
contacts_v17 = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [[]], {'fields': ['id', 'name']})
# print(contacts_v17)

products = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.template', 'search_read', [[]],
                               {'fields': ['id', 'name','detailed_type', 'list_price', 'taxes_id', 'standard_price']})

product_product = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.product', 'search_read', [[]],
                                      {'order' : "id asc"})





# for product in products:
#     print("PRODUCT", product)
#     new_product = {
#         'id' : product.get('id'),
#         'name' : product.get('name'),
#         'type' : 'consu' if product.get('detailed_type') == 'consu' else 'service',
#         'list_price' : product.get('list_price'),
#         'taxes_id' : product.get('taxes_id'),
#         'standard_price' : product.get('standard_price'),
#
#     }
#
#     models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.template', 'create',[new_product])


for prod in product_product:
    # print("Prod",prod)
    # print("iiiiiiiiiiiiidddddddddddd",prod.get('product_template_attribute_value_ids'))
    new_pro = {
        "id" : prod.get('id'),
        'name': prod.get('name'),
        'list_price': prod.get('list_price'),
        'standard_price': prod.get('standard_price'),
        # 'product_tmpl_id' : prod.get('product_tmpl_id')[0],
        'type' : 'consu' if prod.get('detailed_type') == 'consu' else 'service',
        'default_code' : prod.get('default_code')
        # 'product_template_attribute_value_ids' : prod.get('product_template_attribute_value_ids')

    }
    print("PRODUCT", new_pro)
    print("-----------------------------------------------------")

    models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'create',[new_pro])
    # print("PRO",pro)
    print("----------------------------------------------------------------------------")



for contact in contacts_v17:
    new_contact = {
        'id' : contact.get('id'),
        'name' : contact.get('name')
    }

    models_2.execute_kw(db_2, uid_db2, password_db_2,'res.partner', 'create', [new_contact])



for order in purchase_order_v17:

    contact_name = order.get('partner_id')[1]
    print("CONTACT NAME", contact_name)
    new_purchase = {}
    contact = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'search', [[('name', '=', contact_name)]])
    # print("CONTACTTT", contact)
    print("rrrrrrrrrrrrrrr",order)
    new_purchase = {
            'id' : order.get('id'),
            'name': order.get('name'),
            'partner_id': contact[0],
            'date_order': order.get('date_order'),
            'state': order.get('state')
        }
    print("NEW PURCHASE",new_purchase)
    models_2.execute_kw(
        db_2, uid_db2, password_db_2,
        'purchase.order', 'create',
        [new_purchase]
    )


for line in purchase_order_line:
    print("eeeeeeeeeeeeeeeeeeee", line)
    pro = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.product', 'search_read', [[('id', '=' , line.get('product_id')[0])]], {'fields': ['id', 'name', 'default_code']})
    print("PROOO",pro)
    # print("**************************************************************")
    if not pro[0].get('default_code'):
        prod = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'search_read', [[('default_code', '=', pro[0].get('default_code'))]], {'fields': ['id', 'name']})
    else:
        prod = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'search_read', [[('name', '=', pro[0].get('name'))]], {'fields': ['id', 'name']})
    print("PROOO",prod)


    new_purchase_line = {
        'id' : line.get('id'),
        'name' : line.get('name'),
        'product_id' : prod[0].get('id'),
        'product_qty' : line.get('product_qty'),
        'price_unit' : line.get('price_unit'),
        'order_id' : line.get('order_id')[0],

    }
    print("new purchase line", new_purchase_line)
    models_2.execute_kw(db_2, uid_db2, password_db_2,'purchase.order.line', 'create', [new_purchase_line])



