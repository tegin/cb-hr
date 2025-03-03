from openupgradelib import openupgrade


def _fix_employee_private_partner(env):
    openupgrade.logged_query(
        env.cr,
        """
        SELECT id, partner_id, personal_email
        FROM hr_employee
        WHERE partner_id IS NOT NULL
        """,
    )
    for (_employee_id, partner_id, personal_email) in env.cr.fetchall():
        partner = env["res.partner"].browse(partner_id)
        child_vals = {
            "street": partner.street,
            "street2": partner.street2,
            "city": partner.city,
            "state_id": partner.state_id.id,
            "zip": partner.zip,
            "phone": partner.phone,
            "email": personal_email,
            "mobile": partner.mobile,
            "parent_id": partner.id,
            "type": "private",
        }
        partner_vals = {
            "street": False,
            "street2": False,
            "zip": False,
            "city": False,
            "state_id": False,
            "phone": False,
            "mobile": False,
        }
        if "zip_id" in partner._fields:
            partner_vals["zip_id"] = False
        partner.write(partner_vals)
        partner.flush()
        env["res.partner"].create(child_vals)


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env.cr, "account", "14.0.1.1/noupdate_changes.xml")
    report = env.ref("cb_hr_views.hr_employee_print_badge")
    report.unlink_action()
    report.create_action()
    _fix_employee_private_partner(env)
