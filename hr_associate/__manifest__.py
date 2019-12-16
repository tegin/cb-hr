# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Hr Associate',
    'summary': """
        Change employees as associates""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Creu Blanca,Odoo Community Association (OCA)',
    'website': 'www.creublanca.es',
    'depends': [
        'hr'
    ],
    'data': [
        'views/hr_employee.xml',
    ],
    "post_init_hook": "post_init_hook",
}
