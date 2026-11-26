# -*- coding: utf-8 -*-
#############################################################################
#
#    Cyllo.
#
#    Copyright (C) 2024-TODAY Cyllo
#    Author: Ajith V
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
#############################################################################
{
    'name': 'Invoice Format Editor',
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Invoice Format Editor',
    'description': """Invoice Format Editor For Configuring the Invoice Templates""",
    'author': 'Cyllo',
    'company': 'Cyllo',
    'maintainer': 'Cyllo',
    'website': 'https://www.cyllo.com',
    'depends': ['account', 'web', 'sale_management'],
    'data': ['security/ir.model.access.csv',
             'data/design_templates.xml',
             'data/normal_preview_templates.xml',
             'data/modern_preview_templates.xml',
             'data/old_standard_preview_templates.xml',
             'views/doc_layout_views.xml',
             'views/base_document_layout_views.xml',
             'views/custom_external_layout_templates.xml',
             'reports/normal_invoice_templates.xml',
             'reports/modern_invoice_templates.xml',
             'reports/old_standard_invoice_templates.xml',
             'reports/report_invoice_templates.xml',
             'reports/preview_layout_report_templates.xml',
             ],
    'images': ['static/description/banner.jpg'],
    'thumbnail_image': '/static/description/thumbnail.jpg',
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
