# -*- coding: utf-8 -*-
###############################################################################
#
#    Cyllo.
#
#    Copyright (C) 2024-TODAY Cyllo(<https://www.cyllo.com>).
#    Author: MOHAMMED DILSHAD TK
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': "Stock Picking From Invoice",
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'summary': """Stock Picking From Customer/Supplier Invoice""",
    'description': """This Module Enables To Create Stocks Picking From 
     Customer/Supplier Invoice""",
    'author': "Cyllo",
    'company': 'Cyllo',
    'maintainer ': 'Cyllo',
    'website': "https://www.cyllo.com",
    'depends': ['account', 'stock', 'payment'],
    'data': ['views/account_move_views.xml'],
    'images': ['static/description/banner.jpg'],
    'thumbnail_image': '/static/description/thumbnail.jpg',
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
