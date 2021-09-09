# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cb Hr Dms",
    "summary": """
        Link cb_hr with dms""",
    "version": "13.0.1.0.1",
    "license": "AGPL-3",
    "author": "Creu Blanca",
    "website": "www.creublanca.es",
    "depends": ["dms_field", "cb_hr_views"],
    "data": [
        "data/dms_data.xml",
        "views/hr_employee_views.xml",
        "views/res_partner_views.xml",
    ],
}
