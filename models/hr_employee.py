from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    grade = fields.Selection(
        selection=[("A", "A"), ("B", "B"), ("C", "C")],
        string="Grade",
        related="current_version_id.grade",
        readonly=False,
    )

    contract_wage = fields.Monetary(
        string="Contract Wage",
        related="current_version_id.wage",
        readonly=False,
    )
