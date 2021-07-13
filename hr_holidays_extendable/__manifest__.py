# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Hr Holidays Extendable",
    "summary": """
        Allows a certain type of holidays to be extended.""",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/hr",
    "depends": ["hr_holidays_public"],
    "data": [
        "wizards/wizard_extend_holidays.xml",
        "views/hr_leave_views.xml",
        "views/hr_leave_type_views.xml",
    ],
}
