# Copyright 2023 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DmsAddDirectoryTemplate(models.Model):

    _name = "dms.add.directory.template"
    _description = "Dms Add Directory Template"
    _parent_name = "parent_id"
    _parent_order = "name"
    _order = "parent_id, name"

    name = fields.Char(string="Folder Name", required=True)
    is_parent = fields.Boolean(string="Is Parent")
    parent_id = fields.Many2one(
        "dms.add.directory.template",
        string="Parent Folder",
        domain="[('is_parent', '=', True)]",
    )
    child_ids = fields.One2many(
        "dms.add.directory.template", "parent_id", string="Child Folders"
    )

    complete_name = fields.Char("Complete Name", compute="_compute_complete_name")

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for folder in self:
            if folder.parent_id:
                folder.complete_name = "{} / {}".format(
                    folder.parent_id.complete_name,
                    folder.name,
                )
            else:
                folder.complete_name = folder.name
