# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models


class HrEmployeeMedicalExamination(models.Model):

    _inherit = "hr.employee.medical.examination"

    state = fields.Selection(selection_add=[("rejected", "Rejected")])

    year = fields.Integer("Year", default=date.today().year)

    @api.multi
    def back_to_pending(self):
        self.write({"state": "pending"})

    @api.multi
    def to_done(self):
        self.write({"state": "done"})

    @api.multi
    def to_cancelled(self):
        self.write({"state": "cancelled"})

    @api.multi
    def to_rejected(self):
        self.write({"state": "rejected"})
