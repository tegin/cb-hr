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

        rrhh_directory_vals = {
            "is_root_directory": False,
            "parent_id": root_directory.id,
            "name": "EXPEDIENTE",
            "group_ids": [(4, self.storage_id.field_default_group_id.id)],
        }

        pr_directory_vals = {
            "is_root_directory": False,
            "parent_id": root_directory.id,
            "name": "PRL",
            "group_ids": [(4, self.storage_id.field_default_group_id.id)],
        }

        rrhh_directory = self.env["dms.directory"].create(rrhh_directory_vals)
        pr_directory = self.env["dms.directory"].create(pr_directory_vals)

        formaciones_directory_vals = {
            "is_root_directory": False,
            "parent_id": pr_directory.id,
            "name": "FORMACIONES PRL",
            "group_ids": [(4, self.storage_id.field_default_group_id.id)],
        }

        revisiones_directory_vals = {
            "is_root_directory": False,
            "parent_id": pr_directory.id,
            "name": "REVISIONES MÉDICAS",
            "group_ids": [(4, self.storage_id.field_default_group_id.id)],
        }

        formaciones_directory = self.env["dms.directory"].create(
            formaciones_directory_vals
        )
        revisiones_directory = self.env["dms.directory"].create(
            revisiones_directory_vals
        )

        return [
            root_directory,
            rrhh_directory,
            pr_directory,
            formaciones_directory,
            revisiones_directory,
        ]
