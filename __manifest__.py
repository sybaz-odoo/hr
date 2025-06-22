{
    'name': "Salary Register Report",
    'summary': "Salary Register Report",
    'description': """
        Salary Register Report
    """,
    "license": "LGPL-3",
    'author': "Muhammad Saleem",
    'website': "https://sybaz.com/",
    'category': 'Generic Modules/Human Resources',
    'version': '18.0.1.0.1',
    'depends': ['hr_payroll_community'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/salary_register_report_wizard.xml',
        'views/salary_register_report_template.xml',
        'views/salary_register_report_template_pdf.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
