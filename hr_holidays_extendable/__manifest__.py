# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Hr Holidays Extendable",
    "summary": """
        Allows a certain type of holidays to be extended.""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca",
    "website": "https://github.com/tegin/cb-hr",
    "depends": ["hr_holidays_public"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/wizard_extend_holidays.xml",
        "views/hr_leave_views.xml",
        "views/hr_leave_type_views.xml",
    ],
}
