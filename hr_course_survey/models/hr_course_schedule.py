# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrCourseSchedule(models.Model):

    _inherit = "hr.course.schedule"

    examination_survey_id = fields.Many2one("survey.survey")
