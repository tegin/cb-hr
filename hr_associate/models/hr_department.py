# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    manager_id = fields.Many2one(
        domain=[('is_employee', '=', True)]
    )
