# Copyright 2026 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models


class HrApplicant(models.Model):

    _inherit = "hr.applicant"

    def action_applications_email(self):
        self.ensure_one()
        self.env.cr.execute(
            """
        SELECT other.id
          FROM hr_applicant
          JOIN hr_applicant other ON LOWER(other.email_from) = LOWER(hr_applicant.email_from)
            OR other.partner_mobile = hr_applicant.partner_mobile
         WHERE hr_applicant.id in %s
        """,
            (tuple(self.ids),),
        )
        ids = [res["id"] for res in self.env.cr.dictfetchall()]
        return {
            "type": "ir.actions.act_window",
            "name": _("Job Applications"),
            "res_model": self._name,
            "view_mode": "tree,kanban,form,pivot,graph,calendar,activity",
            "domain": [("id", "in", ids)],
            "context": {
                "active_test": False,
                "search_default_stage": 1,
            },
        }
