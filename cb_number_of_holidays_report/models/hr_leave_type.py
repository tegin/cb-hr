# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrLeaveType(models.Model):

    _inherit = "hr.leave.type"

    count_in_holidays_report = fields.Boolean(
        string="Count in holidays report", default=True
    )
