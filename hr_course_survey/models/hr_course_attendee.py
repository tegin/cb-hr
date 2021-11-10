# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models, tools

_logger = logging.getLogger(__name__)


class HrCourseAttendee(models.Model):

    _inherit = "hr.course.attendee"

    survey_answer_id = fields.Many2one("survey.user_input", readonly=True)

    def _get_examination_survey_vals(self):
        vals = {}
        if self.employee_id.user_id:
            vals["user"] = self.employee_id.user_id
        else:
            vals["partner"] = (
                self.employee_id.address_id or self.employee_id.address_home_id
            )
        return vals

    def _notify_survey(self):
        template = self.env.ref(
            "hr_course_survey.mail_template_user_input_invite"
        )
        subject = (
            self.env["mail.template"]
            .with_context(safe=True)
            ._render_template(
                template.subject,
                "survey.user_input",
                self.survey_answer_id.id,
                post_process=True,
            )
        )
        body = self.env["mail.template"]._render_template(
            template.body_html,
            "survey.user_input",
            self.survey_answer_id.id,
            post_process=True,
        )
        # post the message
        mail_values = {
            "email_from": tools.formataddr(
                (self.env.user.name, self.env.user.email)
            ),
            "author_id": self.env.user.partner_id.id,
            "model": None,
            "res_id": None,
            "subject": subject,
            "body_html": body,
            "auto_delete": True,
        }
        if self.survey_answer_id.partner_id:
            mail_values["recipient_ids"] = [
                (4, self.survey_answer_id.partner_id.id)
            ]
        else:
            mail_values["email_to"] = self.survey_answer_id.email

        # optional support of notif_layout in context
        notif_layout = self.env.context.get(
            "notif_layout", self.env.context.get("custom_layout")
        )
        if notif_layout:
            try:
                template = self.env.ref(notif_layout, raise_if_not_found=True)
            except ValueError:
                _logger.warning(
                    "QWeb template %s not found when sending survey mails. "
                    "Sending without layouting." % (notif_layout)
                )
            else:
                template_ctx = {
                    "message": self.env["mail.message"]
                    .sudo()
                    .new(
                        dict(
                            body=mail_values["body_html"],
                            record_name=self.survey_answer_id.survey_id.title,
                        )
                    ),
                    "model_description": self.env["ir.model"]
                    ._get("survey.survey")
                    .display_name,
                    "company": self.env.company,
                }
                body = template.render(
                    template_ctx, engine="ir.qweb", minimal_qcontext=True
                )
                mail_values["body_html"] = self.env[
                    "mail.thread"
                ]._replace_local_links(body)

        return self.env["mail.mail"].sudo().create(mail_values)
