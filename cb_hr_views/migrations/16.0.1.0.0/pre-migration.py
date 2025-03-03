from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Convert Text notes field to Html
    openupgrade.convert_field_to_html(
        env.cr, "hr_contract", "notes", "notes", verbose=False
    )
