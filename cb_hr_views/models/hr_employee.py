from datetime import timedelta
from random import choice
from string import digits

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _name = "hr.employee"
    _inherit = ["mail.activity.mixin", "hr.employee"]

    def name_get(self):
        return super(HrEmployee, self.with_context(not_display_company=True)).name_get()

    def _default_personal_identifier(self):
        pid = None
        while not pid or self.env["hr.employee"].search(
            [("personal_identifier", "=", pid)]
        ):
            pid = "".join(choice(digits) for i in range(8))
        return pid

    partner_id = fields.Many2one(
        "res.partner", required=True, store=True, string="Related partner"
    )
    name = fields.Char(compute=False, related="partner_id.name", readonly=True)
    firstname = fields.Char(related="partner_id.firstname", readonly=False)
    lastname = fields.Char(related="partner_id.lastname", readonly=False)
    lastname2 = fields.Char(related="partner_id.lastname2", readonly=False)

    identification_id_expiration = fields.Date(string="Expiration Date", prefetch=False)
    user_id = fields.Many2one(readonly=True, compute="_compute_user", store=True)
    personal_identifier = fields.Char(
        string="Work's Personal ID",
        default=lambda r: r._default_personal_identifier(),
        readonly=True,
        copy=False,
        groups="hr.group_hr_user",
        prefetch=False,
    )
    work_email = fields.Char(related="partner_id.email", store=True)
    parent_id = fields.Many2one(
        compute="_compute_department_parent_id",
        readonly=True,
        groups="hr.group_hr_user",
        store=True,
    )
    company_id = fields.Many2one(
        related="contract_id.company_id", readonly=True, required=False
    )
    working_hours_type = fields.Selection(
        related="contract_id.working_hours_type",
        groups="hr.group_hr_user",
        readonly=True,
    )
    percentage_of_reduction = fields.Float(
        related="contract_id.percentage_of_reduction",
        groups="hr.group_hr_user",
        readonly=True,
    )
    laboral_category_id = fields.Many2one(
        "hr.laboral.category",
        related="contract_id.laboral_category_id",
        groups="hr.group_hr_user",
        readonly=True,
    )
    locker = fields.Char(prefetch=False)
    address_home_id = fields.Many2one(
        compute="_compute_address_home",
        store=True,
        readonly=True,
    )
    identification_id = fields.Char(
        related="partner_id.vat",
    )
    children = fields.Integer(
        groups="base.group_user",
        compute="_compute_children_count",
        store=True,
        prefetch=False,
    )
    today_schedule = fields.Char(
        compute="_compute_today_schedule", readonly=True, prefetch=False
    )
    contract_id = fields.Many2one(store=True, readonly=True)
    turn = fields.Char(related="contract_id.turn")
    contract_notes = fields.Text(related="contract_id.notes")
    transport_plus = fields.Char(prefetch=False)
    address_id = fields.Many2one(string="Center")
    work_location = fields.Char(string="Location")
    service_start_date = fields.Date(
        related=False,
        compute="_compute_service_start_date",
        store=True,
    )
    private_email = fields.Char(readonly=False)
    phone = fields.Char(readonly=False)
    force_service_computation = fields.Boolean(prefetch=False)
    force_service_start_date = fields.Date(prefetch=False)

    @api.depends("partner_id", "partner_id.child_ids", "partner_id.child_ids.type")
    def _compute_address_home(self):
        for record in self:
            record.address_home_id = record.partner_id.child_ids.filtered(
                lambda r: r.type == "private"
            )[:1]

    @api.depends(
        "contract_ids",
        "contract_ids.date_start",
        "first_contract_id",
        "first_contract_id.date_start",
        "force_service_computation",
        "force_service_start_date",
    )
    def _compute_service_start_date(self):
        for record in self:
            if record.force_service_computation:
                record.service_start_date = record.force_service_start_date
            else:
                record.service_start_date = record.first_contract_id.date_start

    @api.onchange("force_service_computation")
    def _onchange_force_service_computation(self):
        if self.force_service_computation and not self.force_service_start_date:
            self.force_service_start_date = self.first_contract_id.date_start

    @api.depends("department_id", "department_id.manager_id")
    def _compute_department_parent_id(self):
        for record in self:
            parent = False
            department = record.department_id
            while department:
                if department.manager_id and department.manager_id != record:
                    parent = department.manager_id
                    break
                department = department.parent_id
            record.parent_id = parent

    @api.depends("contract_ids")
    def _compute_contract_id(self):
        if self.env.context.get("execute_old_update", False):
            return super()._compute_contract_id()
        Contract = self.env["hr.contract"]
        for employee in self:
            employee.contract_id = Contract.search(
                [("employee_id", "=", employee.id)],
                order="date_start desc",
                limit=1,
            )

    @api.depends("resource_calendar_id")
    def _compute_today_schedule(self):
        now = fields.Datetime.context_timestamp(self, fields.Datetime.now())
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        for record in self:
            calendar = record.resource_calendar_id
            resource = record.resource_id
            intervals = calendar._work_intervals_batch(start, end, resource)[
                resource.id
            ]
            if intervals:
                result = []
                for start, stop, _meta in intervals:
                    result.append(
                        _("from %s to %s")
                        % (start.strftime("%H:%M"), stop.strftime("%H:%M"))
                    )
                if len(result) > 1:
                    result = _(" and ").join([", ".join(result[:-1]), result[-1]])
                else:
                    result = result[0]
                record.today_schedule = _("Working %s") % result
                continue
            record.today_schedule = "This employee doesn't work today"

    @api.depends("relative_ids")
    def _compute_children_count(self):
        child_relation = self.env.ref("hr_employee_relative.relation_child").id
        for record in self:
            record.children = len(
                record.relative_ids.filtered(
                    lambda r: r.relation_id.id == child_relation
                )
            )

    @api.depends("partner_id")
    def _compute_user(self):
        for record in self:
            user_id = self.env["res.users"].search(
                [
                    "|",
                    ("active", "=", True),
                    ("active", "=", False),
                    ("partner_id", "=", record.partner_id.id),
                ],
                limit=1,
            )
            record.user_id = user_id

    @api.onchange("company_id")
    def _onchange_company(self):
        if not self.env.context.get("use_old_onchange"):
            return super()._onchange_company()
        return {}

    def _update_employee_manager(self, manager_id):
        return

    def toggle_active(self):
        super().toggle_active()
        for record in self:
            active = record.active
            contracts = self.env["hr.contract"].search(
                [
                    ("employee_id", "=", record.id),
                    ("state", "not in", ["close", "cancel"]),
                ]
            )
            if not active and contracts:
                raise ValidationError(
                    _("There are running or drafts contracts for %s")
                    % record.display_name
                )
            if record.user_id and record.user_id.active != active:
                record.user_id.with_context(
                    ignore_partner_archive_constrain=True
                ).toggle_active()
            if record.partner_id.active != active:
                record.partner_id.with_context(
                    ignore_partner_archive_constrain=True
                ).toggle_active()

    def action_open_related_partner(self):
        self.ensure_one()
        return self.partner_id.get_formview_action()

    @api.constrains("partner_id")
    def _check_practitioner(self):
        for record in self:
            if not record.partner_id.is_practitioner:
                raise ValidationError(_("All employees must be practitioners"))


class HrEmployeeCalendar(models.Model):
    _inherit = "hr.employee.calendar"
    _order = "date_end desc"


class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    partner_id = fields.Many2one("res.partner")


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    @api.depends()
    def _compute_address_id(self):
        super(
            HrEmployeeBase, self.filtered(lambda r: not r.address_id)
        )._compute_address_id()
