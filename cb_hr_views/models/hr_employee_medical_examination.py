# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrEmployeeMedicalExamination(models.Model):

    _inherit = 'hr.employee.medical.examination'

    state = fields.Selection(selection_add=[('rejected', 'Rejected')])
