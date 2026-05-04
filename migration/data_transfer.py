import xmlrpc.client

url_db1 = "http://127.0.0.1:8017"
db_1 = 'test177'
username_db_1 = '1'
password_db_1 = '1'
common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
version_db1 = common_1.version()



url_db2 = "http://localhost:8019"
db_2 = 'odoo19_test'
username_db_2 = '1'
password_db_2 = '1'
common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
version_db2 = common_2.version()

uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})


purchase_order_v17 = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order', 'search_read', [[]], {'fields': ['id', 'name', 'partner_id','user_id', 'date_order','order_line']})
purchase_order_line = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order.line', 'search_read',[[]])
print("PURCHASE ORDER LINES -------",purchase_order_line[0])

# new_lead = models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'create', [db_1_leads])
contacts_v17 = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [[]], {'fields': ['id', 'name']})
# print(contacts_v17)
products = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.product', 'search_read', [[]],
                               {'fields': ['id', 'name','detailed_type', 'list_price', 'taxes_id', 'standard_price']})

# for line in purchase_order_line:
#
#     new_purchase_line = {
#         'name' :
#     }



for product in products:
    print("PRODUCT", product)
    new_product = {
        'name' : product.get('name'),
        'type' : 'consu' if product.get('detailed_type') == 'consu' else 'service',
        'list_price' : product.get('list_price'),
        'taxes_id' : product.get('taxes_id'),
        'standard_price' : product.get('standard_price')
    }

    models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.product', 'create',[new_product])

for contact in contacts_v17:
    new_contact = {
        'name' : contact.get('name')
    }

    models_2.execute_kw(db_2, uid_db2, password_db_2,'res.partner', 'create', [new_contact])

for order in purchase_order_v17:

    purchase_order_line = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order.line', 'search', [[('id', 'in', order.get('order_line'))]])


    contact_name = order.get('partner_id')[1]
    print("CONTACT NAME", contact_name)
    new_purchase = {}
    contact = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'search', [[('name', '=', contact_name)]])
    print("CONTACTTT", contact)
    new_purchase = {
            'name': order.get('name'),
            'partner_id': contact[0],
            'date_order': order.get('date_order'),
        }
    models_2.execute_kw(
        db_2, uid_db2, password_db_2,
        'purchase.order', 'create',
        [new_purchase]
    )




