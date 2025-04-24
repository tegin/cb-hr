# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime as datetime

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestNumberOfHolidaysReport(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.holiday_type = cls.env["hr.leave.type"].create(
            {
                "name": "Holiday Type",
                "request_unit": "day",
                "requires_allocation": "no",
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
        leave_start_datetime = datetime.date(2019, 8, 5)  # lunes
        leave_end_datetime = datetime.date(2019, 8, 9)  # viernes
        cls.holiday = cls.env["hr.leave"].create(
            {
                "employee_id": cls.employee.id,
                "holiday_status_id": cls.holiday_type.id,
                "date_from": leave_start_datetime,
                "date_to": leave_end_datetime + datetime.timedelta(days=1),
            }
        )

        # print("holidays", cls.holiday.read())
        # cls.holiday = cls.env["hr.leave"].create(
        #     {
        #         "employee_id": cls.employee.id,
        #         "holiday_status_id": cls.holiday_type.id,
        #         "date_from": "2019-08-05",
        #         "date_to": "2019-08-09",
        #     }
        # )
        cls.holiday.action_validate()
        cls.wizard = cls.env["wizard.holidays.count"].create(
            {
                "date_from": "2019-08-04",
                "date_to": "2019-08-11",
                "department_id": cls.department.id,
                "category_ids": [(4, cls.category.id)],
            }
        )

        # print("wizard", cls.wizard.read())

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
        data["form"]["date_to"] = "2019-08-11"
        result = self.env[
            "report.cb_number_of_holidays_report.report_holidays_count"
        ]._get_report_values(False, data)
        self.assertEqual(result["docs"][0]["num_of_days"], 5.0)
        self.assertEqual(result["docs"][0]["employee"], "Pieter")

        data["form"]["date_from"] = "2019-08-07"
        print("data", data)
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
