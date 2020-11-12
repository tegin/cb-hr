# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResourceCalendar(models.Model):

    _inherit = "resource.calendar"

    employee_ids = fields.One2many(
        "hr.employee", inverse_name="resource_calendar_id", readonly=True
    )

    attendance_ids = fields.One2many(
        default=lambda r: r._get_default_attendance_ids()
    )

    def _get_default_attendance_ids(self):
        res = super()._get_default_attendance_ids()
        for line in res:
            line[2].update({"margin_from": 0, "margin_to": 0})
        return res
