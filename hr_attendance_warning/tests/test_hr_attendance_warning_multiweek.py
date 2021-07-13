from datetime import date, datetime

import odoo.tests.common as common
from mock import patch
from odoo import fields


class TestHrAttendanceWarning(common.TransactionCase):
    def _define_calendar_2_weeks(self, name, attendances):
        return self.env["resource.calendar"].create(
            {
                "name": name,
                "two_weeks_calendar": True,
                "attendance_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "%s_%d" % (name, index),
                            "hour_from": att[0],
                            "hour_to": att[1],
                            "dayofweek": str(att[2]),
                            "week_type": att[3],
                            "display_type": att[4],
                            "sequence": att[5],
                            "margin_from": 30,
                            "margin_to": 30,
                        },
                    )
                    for index, att in enumerate(attendances)
                ],
            }
        )

    def setUp(self):
        super(TestHrAttendanceWarning, self).setUp()

        self.calendar_two_weeks = self._define_calendar_2_weeks(
            "Week 1: 24 Hours - Week 2: 43 Hours",
            [
                (8, 16, 0, "0", "line_section", 0),
                (8, 16, 0, "0", False, 1),
                (9, 17, 1, "0", False, 2),
                (7, 20, 0, "1", "line_section", 10),
                (8, 16, 0, "1", False, 11),
                (9, 17, 1, "1", False, 12),
                (7, 15, 2, "1", False, 13),
                (8, 16, 3, "1", False, 14),
                (10, 16, 4, "1", False, 15),
            ],
        )

        self.employee_two_weeks = self.env["hr.employee"].create(
            {
                "name": "Employee",
                "resource_calendar_id": self.calendar_two_weeks.id,
            }
        )

    def test_no_check_in_out_week_1(self):
        with patch("odoo.fields.Datetime.now") as now, patch(
            "odoo.fields.Date.today"
        ) as today:
            now.return_value = datetime(2018, 6, 10, 21, 0, 0, 0)
            today.return_value = date(2018, 6, 10)
            attendances = self.env["resource.calendar.attendance"].search(
                [("calendar_id", "=", self.calendar_two_weeks.id)]
            )
            for att in attendances:
                self.assertFalse(att.next_check_from)
                self.assertFalse(att.next_check_to)

            monday = self.env["resource.calendar.attendance"].search(
                [
                    ("calendar_id", "=", self.calendar_two_weeks.id),
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
                    ("calendar_id", "=", self.calendar_two_weeks.id),
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
                "2018-06-12 09:30:00",
            )
            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        tuesday,
                        fields.Datetime.from_string(tuesday.next_check_to),
                    )
                ),
                "2018-06-12 17:30:00",
            )
            now.return_value = datetime(2018, 6, 17, 21, 0, 0, 0)
            today.return_value = date(2018, 6, 17)
            self.env["resource.calendar.attendance"].cron_attendance_checks()

            warning_in = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee_two_weeks.id)], limit=1
            )

            self.assertFalse(warning_in)

    def test_no_check_in_out_week_2(self):
        with patch("odoo.fields.Datetime.now") as now, patch(
            "odoo.fields.Date.today"
        ) as today:
            now.return_value = datetime(2018, 6, 17, 21, 0, 0, 0)
            today.return_value = date(2018, 6, 17)
            attendances = self.env["resource.calendar.attendance"].search(
                [("calendar_id", "=", self.calendar_two_weeks.id)]
            )
            for att in attendances:
                self.assertFalse(att.next_check_from)
                self.assertFalse(att.next_check_to)

            monday = self.env["resource.calendar.attendance"].search(
                [
                    ("calendar_id", "=", self.calendar_two_weeks.id),
                    ("dayofweek", "=", 0),
                    ("week_type", "=", 1),
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
                "2018-06-18 07:30:00",
            )
            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        monday,
                        fields.Datetime.from_string(monday.next_check_to),
                    )
                ),
                "2018-06-18 20:30:00",
            )

            tuesday = self.env["resource.calendar.attendance"].search(
                [
                    ("calendar_id", "=", self.calendar_two_weeks.id),
                    ("dayofweek", "=", 1),
                    ("week_type", "=", 1),
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
                "2018-06-19 09:30:00",
            )
            self.assertEqual(
                fields.Datetime.to_string(
                    fields.Datetime.context_timestamp(
                        tuesday,
                        fields.Datetime.from_string(tuesday.next_check_to),
                    )
                ),
                "2018-06-19 17:30:00",
            )

            now.return_value = datetime(2018, 6, 19, 21, 0, 0, 0)
            today.return_value = date(2018, 6, 19)
            self.env["resource.calendar.attendance"].cron_attendance_checks()

            warning_in = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee_two_weeks.id)], limit=1
            )
            self.assertTrue(warning_in)
            warning_line = self.env["hr.attendance.warning.line"].search(
                [("warning_id", "=", warning_in.id)], limit=1
            )
            self.assertTrue(warning_line)
            self.assertEqual(warning_line.warning_type, "no_check_in")
            warning_line._compute_message()
            self.assertEqual(
                warning_line.message,
                "Didn't check in between \"2018-06-19"
                ' 08:30:00" and "2018-06-19 09:30:00".',
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
                    ("employee_id", "=", self.employee_two_weeks.id),
                    ("warning_type", "=", "no_check_out"),
                ]
            )

            self.assertEqual(len(warning_out), 1)
            warning_out._compute_message()
            self.assertEqual(
                warning_out.message,
                "Didn't check out between \"2018-06-19 "
                '16:30:00" and "2018-06-19 17:30:00".',
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
                "2018-06-25 07:01:00",
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
                "2018-06-25 20:01:00",
            )

            self.employee_two_weeks.write({"active": False})
            self.employee_two_weeks._create_warning(
                "no_check_out", "2018-06-18"
            )
            warning_out = self.env["hr.attendance.warning.line"].search(
                [
                    ("employee_id", "=", self.employee_two_weeks.id),
                    ("warning_type", "=", "no_check_out"),
                ]
            )

            self.assertEqual(len(warning_out), 1)

    def test_out_of_interval_week_1(self):
        with patch("odoo.fields.Datetime.now") as p:
            p.return_value = datetime(2018, 6, 12, 1, 0, 0, 0)
            self.employee_two_weeks.attendance_action_change()
            att = self.env["hr.attendance"].search(
                [("employee_id", "=", self.employee_two_weeks.id)], limit=1
            )
            warning = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee_two_weeks.id)], limit=1
            )
            self.assertTrue(warning)
            self.assertTrue(att)

            p.return_value = datetime(2018, 6, 12, 19, 0, 0, 0)
            self.employee_two_weeks.attendance_action_change()
            warning = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee_two_weeks.id)], limit=1
            )
            warning_line = self.env["hr.attendance.warning.line"].search(
                [("warning_id", "=", warning.id)], limit=1
            )
            self.assertTrue(warning)
            self.assertEqual(warning.employee_id, self.employee_two_weeks)
            self.assertEqual(warning_line.warning_type, "out_of_interval")

    def test_out_of_interval_week2(self):
        with patch("odoo.fields.Datetime.now") as p:
            p.return_value = datetime(2018, 6, 18, 12, 0, 0, 0)
            self.employee_two_weeks.attendance_action_change()
            att = self.env["hr.attendance"].search(
                [("employee_id", "=", self.employee_two_weeks.id)], limit=1
            )
            warning = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee_two_weeks.id)], limit=1
            )
            self.assertFalse(warning)
            self.assertTrue(att)

            p.return_value = datetime(2018, 6, 18, 19, 0, 0, 0)
            self.employee_two_weeks.attendance_action_change()
            warning = self.env["hr.attendance.warning"].search(
                [("employee_id", "=", self.employee_two_weeks.id)], limit=1
            )
            warning_line = self.env["hr.attendance.warning.line"].search(
                [("warning_id", "=", warning.id)], limit=1
            )
            self.assertTrue(warning)
            self.assertEqual(warning.employee_id, self.employee_two_weeks)
            self.assertEqual(warning_line.warning_type, "out_of_interval")
