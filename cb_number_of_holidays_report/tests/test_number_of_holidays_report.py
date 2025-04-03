# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import Form, TransactionCase


class TestNumberOfHolidaysReport(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.holiday_type = cls.env["hr.leave.type"].create(
            {
                "name": "Holiday Type",
                "request_unit": "day",
                "requires_allocation": "no",
                "validity_start": False,
            }
        )
        cls.partner_id = cls.env["res.partner"].create(
            {"name": "Pieter", "is_practitioner": True}
        )
        cls.department = cls.env["hr.department"].create({"name": "Department"})
        cls.category = cls.env["hr.employee.category"].create({"name": "Tag 1"})
        cls.calendar = cls.env["resource.calendar"].create(
            {"name": "Calendar 1", "attendance_ids": []}
        )
        for i in range(0, 7):
            cls.env["resource.calendar.attendance"].create(
                {
                    "name": "Day " + str(i),
                    "dayofweek": str(i),
                    "hour_from": 8.0,
                    "hour_to": 17.0,
                    "calendar_id": cls.calendar.id,
                }
            )

        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Pieter",
                "partner_id": cls.partner_id.id,
                "department_id": cls.department.id,
                "resource_calendar_id": cls.calendar.id,
                "category_ids": [(4, cls.category.id)],
            }
        )
        f = Form(cls.env["hr.leave"])
        f.employee_id = cls.employee
        f.holiday_status_id = cls.holiday_type
        f.request_date_from = "2019-08-05"
        f.request_date_to = "2019-08-09"
        cls.holiday = f.save()
        cls.holiday.action_validate()
        cls.wizard = cls.env["wizard.holidays.count"].create(
            {
                "date_from": "2019-08-04",
                "date_to": "2019-08-10",
                "department_id": cls.department.id,
                "category_ids": [(4, cls.category.id)],
            }
        )

    def test_number_of_holidays_report(self):
        self.wizard.populate()
        self.assertIn(self.employee.id, self.wizard.employee_ids.ids)
        with self.assertRaises(UserError):
            self.env[
                "report.cb_number_of_holidays_report.report_holidays_count"
            ]._get_report_values(False, {})

        data = dict({"form": {}})
        data["ids"] = self.wizard.ids
        data["model"] = self.wizard._name
        data["form"]["employee_ids"] = [self.employee.id]

        data["form"]["date_from"] = "2019-08-04"
        data["form"]["date_to"] = "2019-08-10"
        result = self.env[
            "report.cb_number_of_holidays_report.report_holidays_count"
        ]._get_report_values(False, data)
        self.assertEqual(result["docs"][0]["num_of_days"], 5.0)
        self.assertEqual(result["docs"][0]["employee"], "Pieter")

        data["form"]["date_from"] = "2019-08-07"
        result = self.env[
            "report.cb_number_of_holidays_report.report_holidays_count"
        ]._get_report_values(False, data)

        self.assertEqual(result["docs"][0]["num_of_days"], 3.0)

        data["form"]["date_to"] = "2019-08-08"
        result = self.env[
            "report.cb_number_of_holidays_report.report_holidays_count"
        ]._get_report_values(False, data)

        self.assertEqual(result["docs"][0]["num_of_days"], 2.0)

        data["form"]["date_from"] = "2019-08-04"
        result = self.env[
            "report.cb_number_of_holidays_report.report_holidays_count"
        ]._get_report_values(False, data)

        self.assertEqual(result["docs"][0]["num_of_days"], 4.0)

        printing = self.wizard.print_report()
        self.assertEqual(
            printing["context"]["report_action"]["report_name"],
            "cb_number_of_holidays_report.report_holidays_count",
        )
        self.assertEqual(
            printing["context"]["report_action"]["data"]["form"]["employee_ids"],
            [self.employee.id],
        )
