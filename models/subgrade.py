from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SubGrade(models.Model):
    _name = 'grade.subgrade'
    _description = 'Sub Grade'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    grade_id = fields.Many2one('grade', string='Grade', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    min_wage = fields.Float(string='Min Wage', required=True)
    max_wage = fields.Float(string='Max Wage', required=True)
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        related='grade_id.company_id',
        store=True,
        readonly=True
    )

    @api.constrains('min_wage', 'max_wage')
    def _check_wage_range(self):
        for subgrade in self:
            if subgrade.min_wage < 0:
                raise ValidationError(_('Minimum wage cannot be negative.'))
            if subgrade.max_wage < subgrade.min_wage:
                raise ValidationError(_('Maximum wage must be greater than or equal to minimum wage.'))
            # Check if subgrade range is within parent grade range
            if subgrade.grade_id.min_wage and subgrade.min_wage < subgrade.grade_id.min_wage:
                raise ValidationError(_('Sub-grade minimum wage cannot be less than the parent grade minimum wage.'))
            if subgrade.grade_id.max_wage and subgrade.max_wage > subgrade.grade_id.max_wage:
                raise ValidationError(_('Sub-grade maximum wage cannot be greater than the parent grade maximum wage.'))
