# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrHolidays(models.Model):

    _name = "hr.holidays"
    _inherit = ["mail.thread", "mail.activity.mixin", "hr.holidays"]

    department_id = fields.Many2one(
        related="employee_id.department_id", readonly=True, store=True
    )

    @api.multi
    def _prepare_holidays_meeting_values(self):
        result = super()._prepare_holidays_meeting_values()
        if not result.get("partner_ids", False):
            result["partner_ids"] = [(4, self.employee_id.partner_id.id)]
        return result

    tree_color = fields.Char(compute="_compute_color", store=True)

    @api.depends("state")
    def _compute_color(self):
        for record in self:
            if record.state == "validate":
                record.tree_color = "#e2ffe6"
            elif record.state == "validate1":
                record.tree_color = "#e2f0ff"
            elif record.state == "refuse":
                record.tree_color = "#ffefef"
            else:
                record.tree_color = "#ffffff"
