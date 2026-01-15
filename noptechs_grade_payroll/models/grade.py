from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class Grade(models.Model):
    _name = 'grade'
    _description = 'Grade'

    name = fields.Char(string='Name')
    category = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ], string='Category', required=True)
    company_id = fields.Many2one(string='Company', comodel_name='res.company', default=lambda self: self.env.company, readonly=True)
    max_wage = fields.Float(string='Max Wage')
    min_wage = fields.Float(string='Min Wage')
    subgrade_ids = fields.One2many('grade.subgrade', 'grade_id', string='Sub Grades')

    _unique_company_category = models.Constraint(
        'unique(company_id, category)',
        'Each company can have only one grade per category (A, B, or C).'
    )

    @api.constrains('category', 'company_id')
    def _check_unique_category_per_company(self):
        """Ensure each company has only one grade per category"""
        for grade in self:
            if not grade.company_id:
                continue
            existing_grade = self.search([
                ('company_id', '=', grade.company_id.id),
                ('category', '=', grade.category),
                ('id', '!=', grade.id)
            ], limit=1)
            if existing_grade:
                raise ValidationError(_(
                    'A grade with category "%s" already exists for company "%s". '
                    'Each company can have only one grade per category.'
                ) % (grade.category, grade.company_id.name))

    @api.constrains('min_wage', 'max_wage')
    def _check_wage_range(self):
        for grade in self:
            if grade.min_wage and grade.min_wage < 0:
                raise ValidationError(_('Minimum wage cannot be negative.'))
            if grade.max_wage and grade.min_wage and grade.max_wage < grade.min_wage:
                raise ValidationError(_('Maximum wage must be greater than or equal to minimum wage.'))
