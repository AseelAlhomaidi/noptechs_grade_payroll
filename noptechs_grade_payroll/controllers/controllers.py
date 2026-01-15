# from odoo import http


# class NoptechsGradePayroll(http.Controller):
#     @http.route('/noptechs_grade_payroll/noptechs_grade_payroll', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/noptechs_grade_payroll/noptechs_grade_payroll/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('noptechs_grade_payroll.listing', {
#             'root': '/noptechs_grade_payroll/noptechs_grade_payroll',
#             'objects': http.request.env['noptechs_grade_payroll.noptechs_grade_payroll'].search([]),
#         })

#     @http.route('/noptechs_grade_payroll/noptechs_grade_payroll/objects/<model("noptechs_grade_payroll.noptechs_grade_payroll"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('noptechs_grade_payroll.object', {
#             'object': obj
#         })

