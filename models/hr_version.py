from odoo import models, api, _
from odoo.exceptions import ValidationError


class HrVersion(models.Model):
    _inherit = 'hr.version'

    @api.constrains('wage')
    def _check_wage_against_grade(self):
        """Validate wage against employee's grade or subgrade range"""
        for version in self:
            employee = version.employee_id
            if not employee or not version.wage:
                continue
            
            wage = version.wage
            
            # If subgrade is selected, validate against subgrade range
            if employee.subgrade_id:
                subgrade = employee.subgrade_id
                if subgrade.min_wage and wage < subgrade.min_wage:
                    raise ValidationError(_(
                        'Wage (%.2f) is below the minimum wage (%.2f) for sub-grade "%s".'
                    ) % (wage, subgrade.min_wage, subgrade.name))
                if subgrade.max_wage and wage > subgrade.max_wage:
                    raise ValidationError(_(
                        'Wage (%.2f) exceeds the maximum wage (%.2f) for sub-grade "%s".'
                    ) % (wage, subgrade.max_wage, subgrade.name))
            # If only grade is selected, validate against grade range
            elif employee.grade_id:
                grade = employee.grade_id
                if grade.min_wage and wage < grade.min_wage:
                    raise ValidationError(_(
                        'Wage (%.2f) is below the minimum wage (%.2f) for grade "%s".'
                    ) % (wage, grade.min_wage, grade.name))
                if grade.max_wage and wage > grade.max_wage:
                    raise ValidationError(_(
                        'Wage (%.2f) exceeds the maximum wage (%.2f) for grade "%s".'
                    ) % (wage, grade.max_wage, grade.name))
