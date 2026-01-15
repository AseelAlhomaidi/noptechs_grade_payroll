from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    grade_id = fields.Many2one(string='Wage Grade', comodel_name='grade')
    subgrade_id = fields.Many2one(
        string='Sub Grade',
        comodel_name='grade.subgrade',
        domain="[('grade_id', '=', grade_id)]",
        help="Select a sub-grade within the selected grade"
    )

    @api.onchange('grade_id')
    def _onchange_grade_id(self):
        """Clear subgrade when grade changes"""
        if self.grade_id:
            # Clear subgrade if it doesn't belong to the new grade
            if self.subgrade_id and self.subgrade_id.grade_id != self.grade_id:
                self.subgrade_id = False
        else:
            # Clear subgrade if no grade is selected
            self.subgrade_id = False

    @api.constrains('grade_id', 'subgrade_id')
    def _check_wage_range_on_grade_change(self):
        """Validate wage when grade or subgrade changes"""
        for employee in self:
            # Get the current version's wage
            current_version = employee.current_version_id
            if not current_version or not current_version.wage:
                continue
            
            wage = current_version.wage
            
            # If subgrade is selected, validate against subgrade range
            if employee.subgrade_id:
                subgrade = employee.subgrade_id
                if subgrade.min_wage and wage < subgrade.min_wage:
                    raise ValidationError(_(
                        'Wage (%.2f) is below the minimum wage (%.2f) for sub-grade "%s". '
                        'Please update the wage or select a different sub-grade.'
                    ) % (wage, subgrade.min_wage, subgrade.name))
                if subgrade.max_wage and wage > subgrade.max_wage:
                    raise ValidationError(_(
                        'Wage (%.2f) exceeds the maximum wage (%.2f) for sub-grade "%s". '
                        'Please update the wage or select a different sub-grade.'
                    ) % (wage, subgrade.max_wage, subgrade.name))
            # If only grade is selected, validate against grade range
            elif employee.grade_id:
                grade = employee.grade_id
                if grade.min_wage and wage < grade.min_wage:
                    raise ValidationError(_(
                        'Wage (%.2f) is below the minimum wage (%.2f) for grade "%s". '
                        'Please update the wage or select a different grade.'
                    ) % (wage, grade.min_wage, grade.name))
                if grade.max_wage and wage > grade.max_wage:
                    raise ValidationError(_(
                        'Wage (%.2f) exceeds the maximum wage (%.2f) for grade "%s". '
                        'Please update the wage or select a different grade.'
                    ) % (wage, grade.max_wage, grade.name))
