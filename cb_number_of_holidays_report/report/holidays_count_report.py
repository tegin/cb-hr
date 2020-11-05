from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from pytz import timezone, utc


class HolidaysCountReport(models.AbstractModel):
    _name = "report.cb_number_of_holidays_report.report_holidays_count"
    _description = "Report of number of holidays"

    @api.model
    def _get_report_values(self, docids, data=None):
        utz = timezone(self.env.user.tz)

        if not data.get("form"):
            raise UserError(
                _("Form content is missing, this report cannot be printed.")
            )

        date_from = data["form"]["date_from"]
        date_to = data["form"]["date_to"]

        docs = []

        for employee in self.env["hr.employee"].browse(
            data["form"]["employee_ids"]
        ):
            holidays = self.env["hr.leave"].search(
                [
                    ("employee_id", "=", employee.id),
                    ("request_date_from", "<=", date_to),
                    ("request_date_to", ">=", date_from),
                    ("state", "=", "validate"),
                    ("count_in_holidays_report", "=", True),
                ]
            )

            days_count = 0.0
            date_from_day = (
                utz.localize(fields.Datetime.from_string(date_from))
                .astimezone(utc)
                .replace(tzinfo=None)
            )

            date_to_day = (
                utz.localize(fields.Datetime.from_string(date_to))
                .astimezone(utc)
                .replace(tzinfo=None)
            )
            date_to_day += timedelta(days=1)
            for holiday in holidays:
                if date_from_day >= holiday.date_from and (
                    date_to_day <= holiday.date_to
                ):
                    days = (date_to_day - date_from_day).days
                elif date_from_day < holiday.date_from and (
                    date_to_day > holiday.date_to
                ):
                    days = abs(holiday.number_of_days)
                elif date_from_day >= holiday.date_from and (
                    date_to_day >= holiday.date_to
                ):
                    days = self.env["hr.leave"]._get_number_of_days(
                        date_from, holiday.date_to, False
                    )
                else:
                    days = self.env["hr.leave"]._get_number_of_days(
                        holiday.date_from,
                        fields.Datetime.to_string(date_to_day),
                        False,
                    )
                days_count += days
            docs.append({"employee": employee.name, "num_of_days": days_count})

        return {
            "doc_ids": data["ids"],
            "doc_model": data["model"],
            "date_from": date_from,
            "date_to": date_to,
            "docs": docs,
        }
