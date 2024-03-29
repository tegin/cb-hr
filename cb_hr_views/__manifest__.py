# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cb Hr Views",
    "summary": """
        Views for HR modules in Creu Blanca""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca",
    "website": "https://github.com/tegin/cb-hr",
    "depends": [
        "base_fontawesome",
        "base_iban",
        "base_report_to_printer",
        "medical_administration_center",
        "crm",
        "hr_attendance_autoclose",
        "hr_attendance_modification_tracking",
        "hr_attendance_report_theoretical_time",
        "hr_contract",
        "hr_employee_service_contract",
        "hr_course",
        "hr_employee_relative",
        "hr_attendance_report_theoretical_time",
        "hr_contract_employee_calendar_planning",
        "medical_administration_practitioner",
        "partner_second_lastname",
        "iot_key_employee_rfid",
        "hr_holidays_extendable",
        "hr_personal_equipment_stock",
        "hr_employee_partner_external",
    ],
    "data": [
        "security/hr_attendance_security.xml",
        "security/hr_employee_security.xml",
        "security/ir.model.access.csv",
        "views/hr_personal_equipment_request.xml",
        "templates/assets.xml",
        "views/hr_laboral_category.xml",
        "reports/hr_attendance_theoretical_time_report_views.xml",
        "reports/report_new_employee.xml",
        "reports/picking_reports.xml",
        "views/resource_calendar_views.xml",
        "views/res_partner.xml",
        "views/res_users_views.xml",
        "views/hr_attendance_module_views.xml",
        "views/hr_contract_views.xml",
        "views/hr_employee_views.xml",
        "views/hr_job_views.xml",
        "views/hr_department_views.xml",
        "views/hr_course_views.xml",
        "views/hr_leave_views.xml",
        "reports/hr_leave_report_calendar.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}
