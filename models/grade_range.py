from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrPayrollGradeRange(models.Model):
    _name = "hr.payroll.grade.range"
    _description = "Grade Range per Salary Structure"
    _order = "structure_id, grade"

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )

    structure_id = fields.Many2one(
        "hr.payroll.structure",
        string="Salary Structure",
        required=True,
        index=True,
        #domain="[('company_id', 'in', [False, company_id])]",
    )

    grade = fields.Selection(
        selection=[("A", "A"), ("B", "B"), ("C", "C")],
        required=True,
        index=True,
    )

    min_basic = fields.Monetary(string="Min Basic Salary", required=True, default=0.0)
    max_basic = fields.Monetary(string="Max Basic Salary", required=True, default=0.0)

    currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id",
        readonly=True,
        store=True,
    )

    _sql_constraints = [
        (
            "uniq_structure_grade_company",
            "unique(structure_id, grade, company_id)",
            "Only one range is allowed per Grade per Salary Structure (per Company).",
        ),
    ]

    @api.constrains("min_basic", "max_basic")
    def _check_min_max(self):
        for rec in self:
            if rec.min_basic < 0 or rec.max_basic < 0:
                raise ValidationError("Min/Max Basic Salary cannot be negative.")
            if rec.max_basic < rec.min_basic:
                raise ValidationError("Max Basic Salary must be greater than or equal to Min Basic Salary.")
