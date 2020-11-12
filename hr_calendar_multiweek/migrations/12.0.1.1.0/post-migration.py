# Copyright 2018 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    for calendar in env["resource.calendar"].search(
        ["|", ("active", "=", True), ("active", "=", False)]
    ):
        calendar.multi_week = any(
            line.calendar_week_number > 1 for line in calendar.attendance_ids
        )
