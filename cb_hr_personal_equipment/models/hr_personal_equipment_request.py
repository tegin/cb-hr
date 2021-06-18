# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class HrPersonalEquipmentRequest(models.Model):

    _inherit = 'hr.personal.equipment.request'

    def action_view_ppe_report(self):
        report = self.env['ir.actions.report']._get_report_from_name(
            'ppe_report')
        return report.report_action(self)
