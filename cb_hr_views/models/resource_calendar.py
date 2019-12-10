# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResourceCalendar(models.Model):

    _inherit = "resource.calendar"

    company_id = fields.Many2one(default=False)
    not_archived = fields.Boolean(default=True)

    @api.multi
    def toggle_archive_calendar(self):
        for record in self:
            record.not_archived = not record.not_archived
