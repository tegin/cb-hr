# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestCbHolidaysMinimumDays(TransactionCase):
    def setUp(self):
        super(TestCbHolidaysMinimumDays, self).setUp()
        self.employee = self.env["hr.employee"].create({"name": "Employee 1"})
        self.holiday_type = (
            self.env["hr.leave.type"]
            .sudo()
            .create(
                {
                    "name": "Leave Type Test",
                    "minimum_time": 7,
                    "validity_start": False,
                }
            )
        )
        self.allocation = (
            self.env["hr.leave.allocation"]
            .sudo()
            .create(
                {
                    "holiday_type": "employee",
                    "employee_id": self.employee.id,
                    "holiday_status_id": self.holiday_type.id,
                    "number_of_days": 10,
                    "state": "validate",
                }
            )
        )

    def test_cb_holidays_minimum_days(self):
        holiday = (
            self.env["hr.leave"]
            .sudo()
            .create(
                {
                    "name": "Test",
                    "employee_id": self.employee.id,
                    "holiday_status_id": self.holiday_type.id,
                    "date_from": "2019-06-19",
                    "date_to": "2019-06-20",
                    "number_of_days": 2,
                    "holiday_type": "employee",
                }
            )
        )

        holiday.action_approve()
        self.assertEqual(
            holiday.warning_minimum,
            "Warning: The number of days requested is less than the"
            " minimum for that holiday type (7)",
        )

        holiday = (
            self.env["hr.leave"]
            .sudo()
            .new(
                {
                    "name": "Test",
                    "employee_id": self.employee.id,
                    "holiday_status_id": self.holiday_type.id,
                    "date_from": "2019-07-10",
                    "date_to": "2019-07-19",
                    "number_of_days": 7,
                }
            )
        )

        self.assertEqual(
            holiday.warning_minimum,
            "Warning: The number of days remaining (1) will"
            " be less than the minimum for that holiday type (7)",
        )
