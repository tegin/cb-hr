# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from mock import patch
from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCbHrViews(TransactionCase):
    def setUp(self):
        super(TestCbHrViews, self).setUp()

        self.partner = self.env["res.partner"].create(
            {
                "name": "Test partner",
                "company_id": False,
                "is_practitioner": True,
            }
        )
        self.partner_2 = self.env["res.partner"].create(
            {
                "name": "Test partner 2",
                "company_id": False,
                "is_practitioner": True,
            }
        )
        self.employee = self.env["hr.employee"].create(
            {
                "name": "John",
                "partner_id": self.partner.id,
                "rfid_card_code": False,
            }
        )
        self.contract = self.env["hr.contract"].create(
            {
                "date_end": fields.Date.to_string(
                    datetime.now() + timedelta(days=365)
                ),
                "date_start": fields.Date.today(),
                "name": "Contract",
                "wage": 5000.0,
                "employee_id": self.employee.id,
                "substituting_id": self.employee.id,
            }
        )

    def test_partner_employee_error(self):
        with self.assertRaises(ValidationError):
            self.employee.partner_id.toggle_active()

    def test_partner_archive(self):
        partner_without_user = self.env["res.partner"].create(
            {"name": "No User"}
        )
        partner_without_user.toggle_active()
        self.assertFalse(partner_without_user.active)
        partner_without_user.toggle_active()
        self.assertTrue(partner_without_user.active)

    def test_employee_archive(self):
        self.employee.regenerate_calendar()
        self.employee.flush()
        self.employee.toggle_active()
        self.assertFalse(self.partner.active)
        self.employee.toggle_active()
        self.assertTrue(self.partner.active)

    def test_show_info(self):
        self.assertTrue(self.partner.show_info)

    def test_is_practitioner_constrain_01(self):
        with self.assertRaises(ValidationError):
            self.partner.write({"is_practitioner": False})

    def test_is_practitioner_constrain_02(self):
        with self.assertRaises(ValidationError):
            self.partner.update({"is_practitioner": False})
            self.employee._check_practitioner()

    def test_employees_constrain(self):
        with self.assertRaises(ValidationError):
            self.partner.write(
                {
                    "employee_ids": [
                        (0, 0, {"name": "Emp", "partner_id": self.partner.id})
                    ]
                }
            )

    def test_employee_creation(self):
        self.partner_2.create_employee()
        employee = self.env["hr.employee"].search(
            [("partner_id", "=", self.partner_2.id)]
        )
        result = self.partner_2.action_open_related_employee()
        self.assertEqual(result["res_id"], employee.id)
        self.env["hr.department"].create(
            {"name": "Department", "manager_id": employee.id}
        )
        employee._compute_is_manager()
        self.assertTrue(employee.manager)

    def test_hr_employee(self):
        self.employee.regenerate_calendar()
        self.employee.flush()
        user_id = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": "user",
                    "login": "login",
                    "email": "email",
                    "partner_id": self.partner.id,
                }
            )
        )

        with self.assertRaises(ValidationError):
            self.employee.partner_id.write({"is_practitioner": False})

        self.employee._compute_show_info()
        self.employee._compute_show_leaves()
        self.assertTrue(self.employee.show_info)
        self.assertTrue(self.employee.show_leaves)

        result = self.employee.action_open_related_partner()
        self.assertEqual(result["res_id"], self.employee.partner_id.id)

        self.employee.toggle_active()
        self.employee.refresh()
        self.assertFalse(self.employee.partner_id.active)
        self.employee.toggle_active()

        self.employee._compute_user()
        self.assertEqual(self.employee.user_id.id, user_id.id)

        self.employee._compute_children_count()
        self.assertEqual(self.employee.children, 0)
        resource_calendar = self.env["resource.calendar"].create(
            {"name": "Resource calendar test"}
        )
        self.employee.resource_calendar_id = resource_calendar.id
        self.employee.resource_calendar_id.write(
            {
                "attendance_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Attendance",
                            "dayofweek": "1",
                            "hour_from": "19",
                            "hour_to": "20",
                        },
                    )
                ]
            }
        )
        with patch("odoo.fields.Datetime.now") as now, patch(
            "odoo.fields.Date.today"
        ) as today:
            now.return_value = fields.Datetime.from_string(
                "2020-05-10 12:00:00"
            )
            today.return_value = fields.Date.from_string("2020-05-10")
            self.employee._compute_today_schedule()
            self.assertEqual(
                self.employee.today_schedule,
                "This employee doesn't work today",
            )

            now.return_value = fields.Datetime.from_string(
                "2020-05-12 12:00:00"
            )
            today.return_value = fields.Date.from_string("2020-05-12")

            self.employee._compute_today_schedule()
            self.assertEqual(
                self.employee.today_schedule,
                "Working from 08:00 to 12:00, from 13:00"
                " to 17:00 and from 19:00 to 20:00",
            )

            self.env["hr.holidays.public"].create(
                {
                    "year": 2020,
                    "line_ids": [
                        (0, 0, {"date": "2020-05-12", "name": "Public"})
                    ],
                }
            )
            self.employee._compute_today_schedule()
            self.assertEqual(
                self.employee.today_schedule,
                "Absent today because of public holidays",
            )

            status = self.env["hr.leave.type"].create(
                {
                    "name": "Sick",
                    "allocation_type": "no",
                    "validity_start": False,
                    "validation_type": "hr",
                }
            )
            holiday = self.env["hr.leave"].create(
                {
                    "name": "Holiday",
                    "employee_id": self.employee.id,
                    "holiday_status_id": status.id,
                    "holiday_type": "employee",
                    "date_from": "2020-05-09 08:00:00",
                    "date_to": "2020-05-17 17:00:00",
                }
            )
            holiday.action_approve()
            self.employee._compute_today_schedule()
            self.assertEqual(
                self.employee.today_schedule, "Out of office since 2020-05-09"
            )

    def test_create_bank_account(self):
        self.assertFalse(self.employee.bank_account_id)
        bank = self.env["res.bank"].create({"name": "bank 1"})
        wizard = (
            self.env["wizard.bank.account.employee"]
            .with_context(active_id=self.employee.id)
            .create({"acc_number": "1234", "bank_id": bank.id})
        )
        with patch(
            "odoo.addons.cb_hr_views.wizards.wizard_bank_account_employee."
            "validate_iban"
        ) as p:
            p.return_value = True
            wizard.create_account()
            p.assert_called()
        self.assertTrue(self.employee.bank_account_id)
