# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, time, timedelta

import pytz
from dateutil import tz
from odoo import api, fields, models


class ResourceCalendarAttendance(models.Model):
    _inherit = "resource.calendar.attendance"

    margin_from = fields.Integer(string="Margin from", default=0)
    margin_to = fields.Integer(string="Margin to", default=0)
    next_check_from = fields.Datetime(default=False)
    next_check_to = fields.Datetime(default=False)

    def _compute_next_check_from(self):
        utz = self.env.user.tz
        now = fields.Datetime.now()
        real_dayofweek = now.weekday()
        diff = int(self.dayofweek) - real_dayofweek
        days = diff if diff >= 0 else 7 + diff
        today = now + timedelta(
            days=days,
            hours=-now.hour,
            minutes=-now.minute,
            seconds=-now.second,
        )
        datetime_tx = (
            (today + timedelta(hours=self.hour_from, minutes=self.margin_from))
            .replace(tzinfo=tz.gettz(utz))
            .astimezone(pytz.utc)
            .replace(tzinfo=None)
        )
        if datetime_tx < now:
            datetime_tx += timedelta(days=7)
        self.next_check_from = datetime_tx

    def _compute_next_check_to(self):
        utz = self.env.user.tz
        now = fields.Datetime.now()
        real_dayofweek = now.weekday()
        diff = int(self.dayofweek) - real_dayofweek
        days = diff if diff >= 0 else 7 + diff
        today = now + timedelta(
            days=days,
            hours=-now.hour,
            minutes=-now.minute,
            seconds=-now.second,
        )
        today.replace(tzinfo=tz.gettz(utz))
        datetime_tx = (
            (today + timedelta(hours=self.hour_to, minutes=self.margin_to))
            .replace(tzinfo=tz.gettz(utz))
            .astimezone(pytz.utc)
            .replace(tzinfo=None)
        )
        if datetime_tx < now:
            datetime_tx += timedelta(days=7)
        self.next_check_to = datetime_tx

    @api.onchange("dayofweek", "hour_from", "margin_from")
    def _onchange_from(self):
        self.next_check_from = False
        if self.margin_from:
            self._compute_next_check_from()

    @api.onchange("dayofweek", "hour_to", "margin_to")
    def _onchange_to(self):
        self.next_check_to = False
        if self.margin_to:
            self._compute_next_check_to()

    def attendances_check_from_domain(self):
        now = fields.Datetime.now()
        today = fields.Date.today()
        return [
            ("margin_from", ">", 0),
            "|",
            ("date_from", "=", False),
            ("date_from", "<=", today),
            "|",
            ("date_to", "=", False),
            ("date_to", ">=", today),
            "|",
            ("next_check_from", "=", False),
            ("next_check_from", "<", now),
        ]

    def attendances_check_to_domain(self):
        now = fields.Datetime.now()
        today = fields.Date.today()
        return [
            ("margin_to", ">", 0),
            "|",
            ("date_from", "=", False),
            ("date_from", "<=", today),
            "|",
            ("date_to", "=", False),
            ("date_to", ">=", today),
            "|",
            ("next_check_to", "=", False),
            ("next_check_to", "<", now),
        ]

    @api.model
    def cron_attendance_checks(self):
        today = fields.Date.today()
        for attendance in self.search(self.attendances_check_from_domain()):
            attendance._check_issue_start(today)
            attendance._compute_next_check_from()

        for attendance in self.search(self.attendances_check_to_domain()):
            attendance._check_issue_end(today)
            attendance._compute_next_check_to()

    def _check_issue_start(self, date):
        date_t = fields.Datetime.from_string(date)
        day_date = fields.Date.from_string(date)
        self.ensure_one()
        # If it's a different day there cannot be a warning.
        if day_date.weekday() != int(self.dayofweek):
            return
        # Special case, attendance until its next check is properly calculated
        if not self.next_check_from:
            return

        employees = self.calendar_id.employee_ids.filtered(
            lambda emp: not self.env["hr.holidays.public"].is_public_holiday(
                day_date, emp.id
            )
        )
        timez = self.env.user.tz
        for employee in employees:
            intervals = self.calendar_id._work_intervals(
                datetime.combine(
                    day_date, time(0, 0, 0, 0, tzinfo=pytz.timezone(timez))
                ),
                datetime.combine(
                    day_date,
                    time(23, 59, 59, 99999, tzinfo=pytz.timezone(timez)),
                ),
                resource=employee.resource_id,
            )
            if any(self in i[2] for i in intervals):
                utz = self.env.user.tz
                min_check_in = date_t + timedelta(
                    hours=self.hour_from, minutes=-self.margin_from
                )
                min_check_in_tz = min_check_in.replace(tzinfo=tz.gettz(utz))
                min_check_in = fields.Datetime.to_string(
                    min_check_in_tz.astimezone(pytz.utc)
                )

                max_check_in = date_t + timedelta(
                    hours=self.hour_from, minutes=self.margin_from
                )
                max_check_in_tz = max_check_in.replace(tzinfo=tz.gettz(utz))
                max_check_in = fields.Datetime.to_string(
                    max_check_in_tz.astimezone(pytz.utc)
                )

                check_in = self.env["hr.attendance"].search(
                    [
                        ("employee_id", "=", employee.id),
                        ("check_in", ">=", min_check_in),
                        ("check_in", "<=", max_check_in),
                    ],
                    order="check_in desc",
                    limit=1,
                )
                if not check_in:
                    employee._create_warning(
                        w_type="no_check_in",
                        min_int=fields.Datetime.to_string(min_check_in_tz),
                        max_int=fields.Datetime.to_string(max_check_in_tz),
                        date=date,
                    )
        return

    def _check_issue_end(self, date):
        date_t = fields.Datetime.from_string(date)

        day_date = fields.Date.from_string(date)
        self.ensure_one()
        # If it's a different day there cannot be a warning.
        if day_date.weekday() != int(self.dayofweek):
            return
        # Special case, attendance until its next check is properly calculated
        if not self.next_check_to:
            return

        employees = self.calendar_id.employee_ids.filtered(
            lambda emp: not self.env["hr.holidays.public"].is_public_holiday(
                day_date, emp.id
            )
        )
        timez = self.env.user.tz
        for employee in employees:
            intervals = self.calendar_id._work_intervals(
                datetime.combine(
                    day_date, time(0, 0, 0, 0, tzinfo=pytz.timezone(timez))
                ),
                datetime.combine(
                    day_date,
                    time(23, 59, 59, 99999, tzinfo=pytz.timezone(timez)),
                ),
                resource=employee.resource_id,
            )
            if any(self in i[2] for i in intervals):
                utz = self.env.user.tz
                min_check_out = date_t + timedelta(
                    hours=self.hour_to, minutes=-self.margin_to
                )
                min_check_out_tz = min_check_out.replace(tzinfo=tz.gettz(utz))
                min_check_out = fields.Datetime.to_string(
                    min_check_out_tz.astimezone(pytz.utc)
                )

                max_check_out = date_t + timedelta(
                    hours=self.hour_to, minutes=self.margin_to
                )
                max_check_out_tz = max_check_out.replace(tzinfo=tz.gettz(utz))
                max_check_out = fields.Datetime.to_string(
                    max_check_out_tz.astimezone(pytz.utc)
                )
                check_out = self.env["hr.attendance"].search(
                    [
                        ("employee_id", "=", employee.id),
                        ("check_out", ">=", min_check_out),
                        ("check_out", "<=", max_check_out),
                    ],
                    order="check_out desc",
                    limit=1,
                )
                if not check_out:
                    employee._create_warning(
                        w_type="no_check_out",
                        min_int=fields.Datetime.to_string(min_check_out_tz),
                        max_int=fields.Datetime.to_string(max_check_out_tz),
                        date=date,
                    )
        return
