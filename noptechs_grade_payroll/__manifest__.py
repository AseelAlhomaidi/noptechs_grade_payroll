{
    'name': "Grade Payroll",

    'summary': "Grade Payroll",

    'description': """
    Grade Payroll
    """,

    'author': "Noptechs",
    'website': "https://www.noptechs.com",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': ["base", "hr", "hr_payroll"],
    'data': [
        "security/ir.model.access.csv",
        "views/grade_views.xml",
        "views/view_employee_form.xml",
    ],
}

