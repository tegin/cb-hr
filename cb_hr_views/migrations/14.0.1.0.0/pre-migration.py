from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE hr_contract
        SET working_hours_type = 'reduced'
        WHERE working_hours_type = 'part'
        """,
    )
