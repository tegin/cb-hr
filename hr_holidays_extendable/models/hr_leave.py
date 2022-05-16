# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrLeave(models.Model):

    _inherit = "hr.leave"

    extendable = fields.Boolean(
        related="holiday_status_id.extendable", store=True, readonly=True
    )

    def _check_date_state(self):
        if not self.env.context.get("no_check_state_date"):
            super(HrLeave, self)._check_date_state()

    def _get_number_of_days(self, date_from, date_to, employee_id):
        """Returns a float equals to the timedelta between two dates given as string.
        We need to modify in order to add the compute_leaves = False
        """
        if not self.env.context.get("no_check_state_date") or not employee_id:
            return super()._get_number_of_days(date_from, date_to, employee_id)
        employee = self.env["hr.employee"].browse(employee_id)
        return employee._get_work_days_data_batch(
            date_from, date_to, compute_leaves=False
        )[employee.id]
