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
