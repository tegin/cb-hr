# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cb Hr Dms",
    "summary": """
        Link cb_hr with dms""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca",
    "website": "https://github.com/tegin/cb-hr",
    "depends": ["dms_field", "cb_hr_views"],
    "data": [
        "data/dms_data.xml",
        "views/hr_employee_views.xml",
        "views/res_partner_views.xml",
    ],
}
