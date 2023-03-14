# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):

    _inherit = "res.partner"

    employee_ids = fields.One2many(
        "hr.employee",
        inverse_name="partner_id",
        context={"active_test": False},
    )
    can_create_employee = fields.Boolean(
        compute="_compute_can_create_employee", store=True
    )
    employee = fields.Boolean(
        compute="_compute_can_create_employee",
        store=True,
        string="Is Employee",
    )

    @api.depends("employee_ids", "is_practitioner")
    def _compute_can_create_employee(self):
        for record in self:
            employees = record.employee_ids
            record.can_create_employee = not employees and record.is_practitioner
            record.employee = employees and record.is_practitioner

    def action_generate_iot_key(self):
        self.ensure_one()
        if not self.is_practitioner:
            raise ValidationError(_("A practitioner is required in order to add a key"))
        if self.employee:
            raise ValidationError(
                _("The key from employees must be managed from employee")
            )
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "iot_rule.iot_key_wizard_act_window"
        )
        key_id = False
        unique_virtual_key = False
        groups = self._get_default_iot_key_groups()
        if self.iot_key_ids:
            key = self.iot_key_ids[:1]
            key_id = key.id
            unique_virtual_key = key.unique_virtual_key
            groups = key.rule_ids.ids
        action["context"] = {
            "default_res_model": self._name,
            "default_res_id": self.id,
            "default_iot_key_id": key_id,
            "default_unique_virtual_key": unique_virtual_key,
            "default_rule_ids": groups,
        }
        return action

    def _get_default_iot_key_groups(self):
        return []

    def toggle_active(self):
        if not self.env.context.get("ignore_partner_archive_constrain", False):
            for record in self:
                if record.employee_ids:
                    raise ValidationError(
                        _(
                            "%s is an employee, archive/unarchive from employee view "
                            "please"
                        )
                        % record.display_name
                    )
        return super().toggle_active()

    @api.constrains("employee_ids", "is_practitioner")
    def _check_employee(self):
        for record in self:
            if record.employee_ids and not record.is_practitioner:
                raise ValidationError(
                    _("In order to be an employee, is required to be a " "practitioner")
                )
            if len(record.employee_ids) > 1:
                raise ValidationError(_("Only one employee for a partner is allowed"))

    def _employee_vals(self):
        return {"partner_id": self.id, "name": self.name}

    def create_employee(self):
        self.ensure_one()
        employee = (
            self.env["hr.employee"]
            .with_context(skip_employee_calendars_required=True)
            .create(self._employee_vals())
        )
        employee._compute_user()
        if self.iot_key_ids:
            self.iot_key_ids.write({"res_model": employee._name, "res_id": employee.id})
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "cb_hr_views.action_open_related_employee"
        )
        result["views"] = [(False, "form")]
        result["res_id"] = employee.id
        return result

    def action_open_related_employee(self):
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "cb_hr_views.action_open_related_employee"
        )
        result["views"] = [(False, "form")]
        result["res_id"] = self.employee_ids[0].id
        return result

    def _check_medical_practitioner(self):
        return super()._check_medical_practitioner() or self.env.user.has_group(
            "hr.group_hr_manager"
        )
