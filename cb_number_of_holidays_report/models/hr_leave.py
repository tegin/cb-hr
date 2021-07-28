# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrLeave(models.Model):

    _inherit = "hr.leave"

    count_in_holidays_report = fields.Boolean(
        related="holiday_status_id.count_in_holidays_report", store=True
    )
