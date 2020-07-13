# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cb Hr Views",
    "summary": """
        Views for HR modules in Creu Blanca""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca",
    "website": "www.creublanca.es",
    "depends": [
        "base_fontawesome",
        "base_iban",
        "base_report_to_printer",
        "cb_departments_chart",
        "cb_medical_administration_center",
        "crm",
        "hr_attendance_modification_tracking",
        "hr_attendance_report_theoretical_time",
        "hr_attendance_warning",
        "hr_calendar_multiweek",
        "hr_contract",
        "hr_course",
        "hr_employee_relative",
        "hr_job_category",
        "hr_attendance_report_theoretical_time",
        "hr_employee_calendar_planning",
        "hr_employee_medical_examination",
        "medical_administration_practitioner",
        "medical_administration_second_lastname",
    ],
    "data": [
        "views/hr_employee_prl.xml",
        "wizards/wizard_bank_account_employee.xml",
        "views/hr_laboral_category.xml",
        "reports/hr_attendance_theoretical_time_report_views.xml",
        "reports/report_new_employee.xml",
        "views/resource_calendar_views.xml",
        "views/res_partner.xml",
        "views/res_users_views.xml",
        "security/hr_attendance_security.xml",
        "security/ir.model.access.csv",
        "security/hr_employee_security.xml",
        "views/hr_attendance_module_views.xml",
        "views/hr_contract_views.xml",
        "views/hr_employee_views.xml",
        "views/hr_job_views.xml",
        "views/hr_department_views.xml",
        "views/hr_course_views.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}
