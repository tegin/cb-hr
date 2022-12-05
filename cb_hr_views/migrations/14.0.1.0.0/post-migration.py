from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env.cr, "account", "14.0.1.1/noupdate_changes.xml")
    report = env.ref("cb_hr_views.hr_employee_print_badge")
    report.unlink_action()
    report.create_action()
