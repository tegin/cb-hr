# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cb Number Of Holidays Report",
    "summary": """
        Report para saber quien tiene vacaciones en un intervalo de tiempo""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca",
    "website": "www.creublanca.es",
    "depends": ["cb_holidays_compute_mix", "cb_hr_views"],
    "data": [
        "views/hr_leave_type.xml",
        "report/holidays_count_report.xml",
        "wizards/wizard_holidays_count.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}
