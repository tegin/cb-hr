# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import api, fields, models
from odoo.modules.module import get_module_resource


class Department(models.Model):
    _name = "hr.department"
    _inherit = "hr.department"

    child_all_count = fields.Integer(
        "Indirect Surbordinates Count",
        compute="_compute_child_all_count",
        store=False,
    )

    @api.model
    def _default_image(self):
        image_path = get_module_resource(
            "hr", "static/src/img", "default_image.png"
        )
        return base64.b64encode(open(image_path, "rb").read())

    image_1024 = fields.Binary(
        "Photo",
        default=_default_image,
        attachment=True,
        help="This field holds the image used as photo for the department,"
        " limited to 1024x1024px.",
        max_width=1024,
        max_height=1024,
    )
    image_128 = fields.Binary(
        "Medium-sized photo",
        attachment=True,
        related="image_1024",
        help="Medium-sized photo of the employee. It is automatically "
        "resized as a 128x128px image, with aspect ratio preserved. "
        "Use this field in form views or some kanban views.",
        store=True,
        max_width=128,
        max_height=128,
    )

    @api.depends("child_ids.child_all_count")
    def _compute_child_all_count(self):
        for department in self:
            department.child_all_count = len(department.child_ids) + sum(
                child.child_all_count for child in department.child_ids
            )
