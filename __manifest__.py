{
    "name": "PayRoll Grade",
    "summary": "Grades on employee contract versions with min/max wage validation per salary structure",
    "description": """
Adds Grade (A/B/C) to the employee contract version (hr.version) and enforces
min/max Contract Wage based on Salary Structure + Grade configuration.
""",
    "author": "Noptechs",
    "website": "https://www.noptechs.com",
    "category": "Payroll",
    "version": "19.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["hr", "hr_payroll"],
    "data": [
        "security/ir.model.access.csv",
        "views/grade_range_views.xml",
        "views/hr_employee_views.xml",
    ],
    "installable": True,
    "application": False,
}
