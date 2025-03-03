# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrJob(models.Model):
    _inherit = "hr.job"

    company_id = fields.Many2one(default=False)
    no_of_recruitment = fields.Integer(default=0)
