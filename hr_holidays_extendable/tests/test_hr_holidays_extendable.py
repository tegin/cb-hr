# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo.tests.common import Form, TransactionCase


class TestHrHolidaysExtendable(TransactionCase):
    def setUp(self):
        super(TestHrHolidaysExtendable, self).setUp()
        self.partner = self.env["res.partner"].create(
            {"name": "Test partner", "company_id": False}
        )
        self.employee = self.env["hr.employee"].create(
            {"name": "Employee 1", "user_partner_id": self.partner.id}
        )
        self.holiday_type = self.env["hr.leave.type"].create(
            {
                "name": "Leave Type Test",
                "extendable": True,
                "allocation_type": "fixed",
                "validity_start": False,
            }
        )
        self.allocation = self.env["hr.leave.allocation"].create(
            {
                "name": "Test",
                "employee_id": self.employee.id,
                "holiday_status_id": self.holiday_type.id,
                "number_of_days": 10,
            }
        )
        self.allocation.action_validate()

    def test_hr_holidays_extendable(self):

        holiday = Form(self.env["hr.leave"])
        holiday.name = "Test"
        holiday.employee_id = self.employee
        holiday.holiday_status_id = self.holiday_type
        holiday.request_date_from = date(2019, 5, 21)
        holiday.request_date_to = date(2019, 5, 22)
        holiday = holiday.save()
        holiday.action_validate()

        remaining_days = self.holiday_type.get_days(self.employee.id)[
            self.holiday_type.id
        ]["remaining_leaves"]
        self.assertEqual(remaining_days, 8)

        wizard = (
            self.env["wizard.extend.holidays"]
            .with_context({"active_id": holiday.id})
            .create({})
        )
        self.assertEqual(wizard.holidays_id.id, holiday.id)
        wizard.write({"date_to": date(2019, 5, 23)})
        self.assertEqual(wizard.number_of_days, 3)
        wizard.extend_holidays()

        self.assertEqual(holiday.request_date_to, date(2019, 5, 23))
        self.assertEqual(holiday.number_of_days, 3)
        remaining_days = self.holiday_type.get_days(self.employee.id)[
            self.holiday_type.id
        ]["remaining_leaves"]
        self.assertEqual(remaining_days, 7)
