# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResUsers(models.Model):

    _inherit = "res.users"

    @api.model
    def _employee_ids_domain(self):
        # employee_ids is considered a safe field and as such will be fetched as sudo.
        # So try to enforce the security rules on the field to make sure we do not load
        # employees outside of active companies
        return [
            (
                "company_id",
                "in",
                self.env.companies.ids
                + self.env.context.get("allowed_company_ids", []),
            )
        ]

    # note: a user can only be linked to one employee per company (see sql constraint in
    # ´hr.employee´)
    employee_ids = fields.One2many(domain=lambda r: r._employee_ids_domain())
    notification_type = fields.Selection(default="inbox")

    @api.depends("employee_ids")
    @api.depends_context("force_company")
    def _compute_company_employee(self):
        for user in self:
            user.employee_id = self.env["hr.employee"].search(
                [("id", "in", user.employee_ids.ids)], limit=1
            )

    def name_get(self):
        return super(ResUsers, self.with_context(not_display_company=True)).name_get()

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.partner_id.employee_ids:
            res.partner_id.employee_ids._compute_user()
        return res
