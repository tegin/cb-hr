# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResourceCalendar(models.Model):

    _inherit = "resource.calendar"

    def propagate_mondays(self):
        for record in self:
            self.env["resource.calendar.attendance"].search(
                [("dayofweek", "!=", "0"), ("calendar_id", "=", record.id)]
            ).unlink()
            attendances = record.attendance_ids
            for attendance in attendances:
                for i in range(1, 5):
                    values = attendance.copy_data({"dayofweek": str(i)})
                    self.env["resource.calendar.attendance"].create(values[0])


class ResourceCalendarAttendance(models.Model):

    _inherit = "resource.calendar.attendance"

    name = fields.Char(default="Attendance Line")
