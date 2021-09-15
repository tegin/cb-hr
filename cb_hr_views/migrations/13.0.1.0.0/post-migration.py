# Copyright 2021 Creu Blanca - Alba Riera

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE hr_contract hc
        SET substitute_contract = hct.substitute_contract
        FROM hr_contract_type hct
        WHERE hct.id = am.old_type_id""",
    )
