from odoo import fields, models


class HrWorkLocation(models.Model):
    _inherit = "hr.work.location"

    company_id = fields.Many2one(
        "res.company", required=False, default=lambda self: self.env.company
    )
