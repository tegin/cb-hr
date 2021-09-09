# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    access_group = env.ref("cb_hr_dms.hr_access_group")
    for storage_id in [
        "cb_hr_dms.storage_employee",
        "cb_hr_dms.storage_practitioners",
    ]:
        storage = env.ref(storage_id)
        storage.field_default_group_id = access_group
