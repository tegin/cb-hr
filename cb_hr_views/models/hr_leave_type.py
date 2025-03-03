# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrLeaveType(models.Model):

    _inherit = "hr.leave.type"
    create_calendar_meeting = fields.Boolean(default=False)
    company_id = fields.Many2one(default=False)
