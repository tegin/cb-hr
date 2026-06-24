from datetime import datetime, time

import pytz
from pytz import timezone

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HolidaysCountReport(models.AbstractModel):
    _name = "report.cb_number_of_holidays_report.report_holidays_count"
    _description = "Report of number of holidays"

    @api.model
    def _get_report_values(self, docids, data=None):
        timezone(self.env.user.tz)

        if not data.get("form"):
            raise UserError(
                _("Form content is missing, this report cannot be printed.")
            )

        date_from = fields.Datetime.from_string(data["form"]["date_from"])
        date_to = fields.Datetime.from_string(data["form"]["date_to"])

        print("date_from", date_from)
        print("date_to", date_to)

        docs = []
        for employee in self.env["hr.employee"].browse(data["form"]["employee_ids"]):
            print(employee.name)
            tz = employee.resource_id.calendar_id.tz
            holidays = self.env["hr.leave"].search(
                [
                    ("employee_id", "=", employee.id),
                    ("date_from", "<=", date_to),
                    ("date_to", ">=", date_from),
                    ("state", "=", "validate"),
                    ("count_in_holidays_report", "=", True),
                ]
            )

            print("holidays empleadoooooooo", holidays[0].read())

            days_count = 0.0
            # date_from_day = (
            #     utz.localize(date_from)
            #     .astimezone(utc)
            #     .replace(tzinfo=None)
            # )
            date_from_day = datetime.combine(
                date_from, time(0, 0, 0, 0, tzinfo=pytz.timezone(tz))
            )

            # date_to_day = (
            #     utz.localize(date_to)
            #     .astimezone(utc)
            #     .replace(tzinfo=None)
            # )
            date_to_day = datetime.combine(
                date_to, time(23, 59, 59, 99999, tzinfo=pytz.timezone(tz))
            )

            print("date_from_day", date_from_day)
            print("date_to_day", date_to_day)
            print("holidays", holidays[0].date_from)
            print("holidays", holidays[0].date_to)
            # date_to_day += timedelta(days=1)
            for holiday in holidays:
                if date_from_day >= holiday.date_from and (
                    date_to_day <= holiday.date_to
                ):
                    print("1111111111111111111111111")
                    print("number_of_days", holiday.number_of_days)
                    days = (date_to_day - date_from_day).days
                elif date_from_day < holiday.date_from and (
                    date_to_day > holiday.date_to
                ):
                    print("2222222222222222222222222")
                    print("number_of_days", holiday.number_of_days)

                    days = abs(holiday.number_of_days)
                elif date_from_day >= holiday.date_from and (
                    date_to_day >= holiday.date_to
                ):
                    days = self.env["hr.leave"]._get_number_of_days(
                        fields.Datetime.from_string(date_from),
                        holiday.date_to,
                        holiday.employee_id.id,
                    )["days"]
                    print("days", days)
                else:
                    print("44444444444444444444444")
                    print("number_of_days", holiday.number_of_days)

                    days = self.env["hr.leave"]._get_number_of_days(
                        holiday.date_from,
                        fields.Datetime.from_string(date_to_day),
                        holiday.employee_id.id,
                    )["days"]
                days_count += days
            docs.append({"employee": employee.name, "num_of_days": days_count})

        return {
            "doc_ids": data["ids"],
            "doc_model": data["model"],
            "date_from": date_from,
            "date_to": date_to,
            "docs": docs,
        }
