# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrContract(models.Model):

    _inherit = "hr.contract"

    working_hours_type = fields.Selection(
        selection=[
            ("full", "Full Time"),
            ("reduced", "Reduced"),
        ],
        string="Working Hours Type",
        default="full",
        tracking=True,
    )
    percentage_of_reduction = fields.Float("Percentage of Reduction", tracking=True)
    # Propose a number of hours? Maybe related to company

    substituting_id = fields.Many2one("hr.employee", "Substituting", tracking=True)
    substitute_contract = fields.Boolean(
        string="Substitute Contract",
        help="Check if this is a substitution contract",
        tracking=True,
    )
    laboral_category_id = fields.Many2one("hr.laboral.category")

    # Track Visibility
    job_id = fields.Many2one(tracking=True)
    company_id = fields.Many2one(tracking=True)
    date_start = fields.Date(tracking=True)
    date_end = fields.Date(tracking=True)
    trial_date_end = fields.Date(tracking=True)
    department_id = fields.Many2one(tracking=True)
    employee_id = fields.Many2one(tracking=True, required=True)
    name = fields.Char(tracking=True)

    turn = fields.Char()

    @api.onchange("substitute_contract")
    def _onchange_substitute_contract(self):
        for record in self:
            if not record.substitute_contract:
                record.substituting_id = False

    def write(self, vals):
        res = super().write(vals)
        for record in self.filtered("employee_id"):
            record.employee_id._compute_contract_id()
        return res
