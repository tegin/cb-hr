# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):

    _inherit = "res.partner"

    employee_ids = fields.One2many(
        "hr.employee",
        inverse_name="partner_id",
        domain=["|", ("active", "=", True), ("active", "=", False)],
    )
    can_create_employee = fields.Boolean(
        compute="_compute_can_create_employee"
    )
    employee = fields.Boolean(
        compute="_compute_can_create_employee",
        store=True,
        string="Is Employee",
    )

    show_info = fields.Boolean(compute="_compute_show_info", default=True)

    def _compute_show_info(self):
        is_manager = self.env.user.has_group("hr.group_hr_manager")
        for partner in self:
            partner.show_info = is_manager or not partner.employee

    @api.multi
    def toggle_active_modified(self):
        for record in self:

            active = not record.active
            user_ids = self.env["res.users"].search(
                [
                    "|",
                    ("active", "=", True),
                    ("active", "=", False),
                    ("partner_id", "=", record.id),
                ]
            )
            if user_ids:
                user_ids.write({"active": active})
            if not user_ids or not active:
                record.toggle_active()

    @api.depends("employee_ids", "is_practitioner")
    def _compute_can_create_employee(self):
        for record in self:
            employees = self.env["hr.employee"].search(
                [
                    "|",
                    ("active", "=", True),
                    ("active", "=", False),
                    ("partner_id", "=", record.id),
                ]
            )
            record.can_create_employee = (
                not employees and record.is_practitioner
            )
            record.employee = len(employees) > 0 and record.is_practitioner

    @api.constrains("employee_ids", "is_practitioner")
    def _check_employee(self):
        for record in self:
            if record.employee_ids and not record.is_practitioner:
                raise ValidationError(
                    _(
                        "In order to be an employee, is required to be a "
                        "practitioner"
                    )
                )
            if len(record.employee_ids) > 1:
                raise ValidationError(
                    _("Only one employee for a partner is allowed")
                )

    def _employee_vals(self):
        return {"partner_id": self.id, "name": self.name}

    @api.multi
    def create_employee(self):
        employee = self.env["hr.employee"].create(self._employee_vals())
        employee.regenerate_calendar()
        employee._compute_user()
        action = self.env.ref("cb_hr_views.action_open_related_employee")
        result = action.read()[0]
        result["views"] = [(False, "form")]
        result["res_id"] = employee.id
        return result

    @api.multi
    def action_open_related_employee(self):
        action = self.env.ref("cb_hr_views.action_open_related_employee")
        result = action.read()[0]
        result["views"] = [(False, "form")]
        result["res_id"] = self.employee_ids[0].id
        return result
