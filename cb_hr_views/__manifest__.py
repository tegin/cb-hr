# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cb Hr Views",
    "summary": """
        Views for HR modules in Creu Blanca""",
    "version": "11.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca",
    "website": "www.creublanca.es",
    "depends": [
        "base_fontawesome",
        "hr_attendance",
        "hr_contract",
        "hr_family",
        "hr_job_category",
        "hr_course",
        "hr_attendance_report_theoretical_time",
        "hr_employee_calendar_planning",
        "hr_employee_medical_examination",
        "medical_administration_second_lastname",
        "medical_administration_practitioner",
        "cb_medical_administration_center",
        "cb_departments_chart",
        "base_iban",
        "base_report_to_printer",
    ],
    "data": [
        "views/hr_employee_prl.xml",
        "wizards/wizard_bank_account_employee.xml",
        "views/hr_laboral_category.xml",
        "views/hr_holidays_views.xml",
        "reports/hr_attendance_theoretical_time_report_views.xml",
        "views/resource_calendar_views.xml",
        "views/res_partner.xml",
        "views/res_users_views.xml",
        "security/hr_attendance_security.xml",
        "security/ir.model.access.csv",
        "security/hr_employee_security.xml",
        "views/hr_attendance_module_views.xml",
        "views/hr_contract_views.xml",
        "views/hr_employee_views.xml",
        "views/hr_employee_medical_examination.xml",
        "views/hr_job_views.xml",
        "views/hr_department_views.xml",
        "views/hr_course_views.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}
