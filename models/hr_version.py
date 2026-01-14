from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HrVersion(models.Model):
    _inherit = "hr.version"

    grade = fields.Selection(
        selection=[("A", "A"), ("B", "B"), ("C", "C")],
        string="Grade",
        compute="_compute_grade_from_wage",
        store=True,
        readonly=False,   # allow manual override if you want
        tracking=True,
    )

    @api.depends("wage", "structure_id", "structure_type_id", "company_id")
    def _compute_grade_from_wage(self):
        for v in self:
            v.grade = v.grade or "A"  # fallback if you want something when no wage
            if v.wage is None:
                continue

            structure = v.structure_id or (v.structure_type_id.default_struct_id if v.structure_type_id else False)
            if not structure:
                continue

            ranges = self.env["hr.payroll.grade.range"].search([
                ("company_id", "=", v.company_id.id),
                ("structure_id", "=", structure.id),
            ])

            match = ranges.filtered(lambda r: r.min_basic <= v.wage <= r.max_basic)[:1]
            if match:
                v.grade = match.grade
            else:
                # if no grade fits wage, clear grade so user sees it’s invalid
                v.grade = False


    @api.constrains("wage", "grade", "structure_id", "structure_type_id", "company_id")
    def _check_wage_grade_range(self):
        for v in self:
            if v.wage is None:
                continue

            structure = v.structure_id or (v.structure_type_id.default_struct_id if v.structure_type_id else False)
            if not structure:
                continue

            ranges = self.env["hr.payroll.grade.range"].search([
                ("company_id", "=", v.company_id.id),
                ("structure_id", "=", structure.id),
            ])

            if not ranges:
                raise ValidationError(_(
                    "No grade ranges are configured for this Structure.\n\n"
                    "Structure: %(structure)s",
                    structure=structure.name,
                ))

            # If grade is empty or doesn't match wage -> error with the correct matching ranges
            match = ranges.filtered(lambda r: r.min_basic <= v.wage <= r.max_basic)[:1]
            if not match:
                raise ValidationError(_(
                    "The Wage does not fall into any configured grade range.\n\n"
                    "Structure: %(structure)s\n"
                    "Entered Wage: %(wage).2f",
                    structure=structure.name,
                    wage=v.wage,
                ))

            # If user manually set grade different from computed match, block
            if v.grade and v.grade != match.grade:
                raise ValidationError(_(
                    "Selected Grade does not match the Wage range.\n\n"
                    "Structure: %(structure)s\n"
                    "Expected Grade: %(expected)s\n"
                    "Selected Grade: %(selected)s\n"
                    "Entered Wage: %(wage).2f",
                    structure=structure.name,
                    expected=match.grade,
                    selected=v.grade,
                    wage=v.wage,
                ))

