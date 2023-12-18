# Copyright 2023 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DmsAddDirectoryRecord(models.TransientModel):

    _inherit = "dms.add.directory.record"

    with_default_dms_structure = fields.Boolean(
        default=True, string="RRHH default structure"
    )

    def create_directory(self):
        self.ensure_one()
        if self.with_default_dms_structure:
            directories = self._create_default_structure()
            return [directory.id for directory in directories]
        else:
            return super().create_directory()

    def _create_default_structure(self):
        root_directory_vals = self._create_directory_vals()
        root_directory = self.env["dms.directory"].create(root_directory_vals)

        def create_directory_recursively(template_directory, parent_directory):
            directory_vals = {
                "is_root_directory": False,
                "parent_id": parent_directory.id,
                "name": template_directory.name,
                "group_ids": [(4, self.storage_id.field_default_group_id.id)],
            }
            directory = self.env["dms.directory"].create(directory_vals)

            for child in template_directory.child_ids:
                create_directory_recursively(child, directory)

        template_directories = self.env["dms.add.directory.template"].search(
            [
                ("is_parent", "=", True),
                ("parent_id", "=", False),
            ]
        )

        directories = []
        for template_directory in template_directories:
            create_directory_recursively(template_directory, root_directory)
            directories.append(root_directory)
        return directories
