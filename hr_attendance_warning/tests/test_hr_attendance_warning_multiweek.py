from datetime import date, datetime

import odoo.tests.common as common
from mock import patch
from odoo import fields


class TestHrAttendanceWarning(common.TransactionCase):
    def setUp(self):
        super(TestHrAttendanceWarning, self).setUp()

        self.calendar = self.env["resource.calendar"].create(
            {"name": "Calendar 1", "attendance_ids": [], "multi_week": True}
        )

        for i in range(0, 7):
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Day " + str(i),
                    "dayofweek": str(i),
                    "hour_from": 8.0,
                    "hour_to": 16.0,
                    "margin_from": 30,
                    "margin_to": 30,
                    "calendar_id": self.calendar.id,
                    "calendar_week_number": 2,
                    "week_number": 1,
                }
            )

        self.employee = self.env["hr.employee"].create(
            {"name": "Employee", "resource_calendar_id": self.calendar.id}
        )

    def test_no_check_in_out_week_1(self):
        with patch("odoo.fields.Datetime.now") as now, patch(
            "odoo.fields.Date.today"
        ) as today:
            now.return_value = datetime(2018, 6, 10, 21, 0, 0, 0)
            today.return_value = date(2018, 6, 10)
            attendances = self.env["resource.calendar.attendance"].search(
                [("calendar_id", "=", self.calendar.id)]
            )
            for att in attendances:
                self.assertFalse(att.next_check_from)
                self.assertFalse(att.next_check_to)

            monday = self.env["resource.calendar.attendance"].search(
                [
                    ("calendar_id", "=", self.calendar.id),
                    ("dayofweek", "=", 0),
                ],
                limit=1,
            )
            self.env["resource.calendar.attendance"].cron_attendance_checks()

            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        monday,
                        fields.Datetime.from_string(monday.next_check_from),
                    )
                ),
                "2018-06-11 08:30:00",
            )
            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        monday,
                        fields.Datetime.from_string(monday.next_check_to),
                    )
                ),
                "2018-06-11 16:30:00",
            )

            tuesday = self.env["resource.calendar.attendance"].search(
                [
                    ("calendar_id", "=", self.calendar.id),
                    ("dayofweek", "=", 1),
                ],
                limit=1,
            )

            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        tuesday,
                        fields.Datetime.from_string(tuesday.next_check_from),
                    )
                ),
                "2018-06-12 08:30:00",
            )
            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        tuesday,
                        fields.Datetime.from_string(tuesday.next_check_to),
                    )
                ),
                "2018-06-12 16:30:00",
            )
            now.return_value = datetime(2018, 6, 17, 21, 0, 0, 0)
            today.return_value = date(2018, 6, 17)
            self.env["resource.calendar.attendance"].cron_attendance_checks()

            warning_in = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee.id)], limit=1
            )
            self.assertFalse(warning_in)

    def test_no_check_in_out_week_2(self):
        self.calendar.attendance_ids.write({"week_number": 2})
        with patch("odoo.fields.Datetime.now") as now, patch(
            "odoo.fields.Date.today"
        ) as today:
            now.return_value = datetime(2018, 6, 10, 21, 0, 0, 0)
            today.return_value = date(2018, 6, 10)
            attendances = self.env["resource.calendar.attendance"].search(
                [("calendar_id", "=", self.calendar.id)]
            )
            for att in attendances:
                self.assertFalse(att.next_check_from)
                self.assertFalse(att.next_check_to)

            monday = self.env["resource.calendar.attendance"].search(
                [
                    ("calendar_id", "=", self.calendar.id),
                    ("dayofweek", "=", 0),
                ],
                limit=1,
            )
            self.env["resource.calendar.attendance"].cron_attendance_checks()

            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        monday,
                        fields.Datetime.from_string(monday.next_check_from),
                    )
                ),
                "2018-06-11 08:30:00",
            )
            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        monday,
                        fields.Datetime.from_string(monday.next_check_to),
                    )
                ),
                "2018-06-11 16:30:00",
            )

            tuesday = self.env["resource.calendar.attendance"].search(
                [
                    ("calendar_id", "=", self.calendar.id),
                    ("dayofweek", "=", 1),
                ],
                limit=1,
            )

            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        tuesday,
                        fields.Datetime.from_string(tuesday.next_check_from),
                    )
                ),
                "2018-06-12 08:30:00",
            )
            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        tuesday,
                        fields.Datetime.from_string(tuesday.next_check_to),
                    )
                ),
                "2018-06-12 16:30:00",
            )
            now.return_value = datetime(2018, 6, 17, 21, 0, 0, 0)
            today.return_value = date(2018, 6, 17)
            self.env["resource.calendar.attendance"].cron_attendance_checks()

            warning_in = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee.id)], limit=1
            )
            warning_line = self.env["hr.attendance.warning.line"].search(
                [("warning_id", "=", warning_in.id)], limit=1
            )
            self.assertTrue(warning_line)
            self.assertEqual(warning_line.warning_type, "no_check_in")
            warning_line._compute_message()
            self.assertEqual(
                warning_line.message,
                "Didn't check in between \"2018-06-17"
                ' 07:30:00" and "2018-06-17 08:30:00".',
            )

            warning_in.pending2solved()
            self.assertEqual(warning_in.state, "solved")
            warning_in.solved2pending()
            self.assertEqual(warning_in.state, "pending")

            monday.write({"margin_to": False})
            monday._onchange_to()

            monday._check_issue_end(fields.Datetime.now())
            self.env["resource.calendar.attendance"].cron_attendance_checks()

            warning_out = self.env["hr.attendance.warning.line"].search(
                [
                    ("employee_id", "=", self.employee.id),
                    ("warning_type", "=", "no_check_out"),
                ]
            )

            self.assertEqual(len(warning_out), 1)
            warning_out._compute_message()
            self.assertEqual(
                warning_out.message,
                "Didn't check out between \"2018-06-17 "
                '15:30:00" and "2018-06-17 16:30:00".',
            )

            monday.margin_from = 1
            monday._onchange_from()
            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        monday,
                        fields.Datetime.from_string(monday.next_check_from),
                    )
                ),
                "2018-06-18 08:01:00",
            )

            monday.margin_to = 1
            monday._onchange_to()
            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        monday,
                        fields.Datetime.from_string(monday.next_check_to),
                    )
                ),
                "2018-06-18 16:01:00",
            )

            self.employee.write({"active": False})
            self.employee._create_warning("no_check_out", "2018-06-18")
            warning_out = self.env["hr.attendance.warning.line"].search(
                [
                    ("employee_id", "=", self.employee.id),
                    ("warning_type", "=", "no_check_out"),
                ]
            )

            self.assertEqual(len(warning_out), 1)

    def test_out_of_interval_week_1(self):
        with patch("odoo.fields.Datetime.now") as p:
            p.return_value = datetime(2018, 6, 15, 12, 0, 0, 0)
            self.employee.attendance_action_change()
            att = self.env["hr.attendance"].search(
                [("employee_id", "=", self.employee.id)], limit=1
            )
            warning = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee.id)], limit=1
            )
            self.assertTrue(warning)
            self.assertTrue(att)

            p.return_value = datetime(2018, 6, 15, 19, 0, 0, 0)
            self.employee.attendance_action_change()
            warning = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee.id)], limit=1
            )
            warning_line = self.env["hr.attendance.warning.line"].search(
                [("warning_id", "=", warning.id)], limit=1
            )
            self.assertTrue(warning)
            self.assertEqual(warning.employee_id, self.employee)
            self.assertEqual(warning_line.warning_type, "out_of_interval")

    def test_out_of_interval_week2(self):
        self.calendar.attendance_ids.write({"week_number": 2})
        with patch("odoo.fields.Datetime.now") as p:
            p.return_value = datetime(2018, 6, 15, 12, 0, 0, 0)
            self.employee.attendance_action_change()
            att = self.env["hr.attendance"].search(
                [("employee_id", "=", self.employee.id)], limit=1
            )
            warning = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee.id)], limit=1
            )
            self.assertFalse(warning)
            self.assertTrue(att)

            p.return_value = datetime(2018, 6, 15, 19, 0, 0, 0)
            self.employee.attendance_action_change()
            warning = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee.id)], limit=1
            )
            warning_line = self.env["hr.attendance.warning.line"].search(
                [("warning_id", "=", warning.id)], limit=1
            )
            self.assertTrue(warning)
            self.assertEqual(warning.employee_id, self.employee)
            self.assertEqual(warning_line.warning_type, "out_of_interval")
