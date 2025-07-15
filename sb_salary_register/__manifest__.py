{
    'name': "Salary Register Report",
    'summary': "Salary Register Report",
    'description': """
        Salary Register Report
    """,
    "license": "LGPL-3",
    'author': "Sybaz",
    'website': "https://sybaz.com/",
    'category': 'Generic Modules/Human Resources',
    'version': '17.0.1.0.1',
    'depends': ['hr_payroll_community'],
    'company': 'Sybaz',
    'maintainer': 'Sybaz',
    'data': [
        'security/ir.model.access.csv',
        'wizard/salary_register_report_wizard.xml',
        'views/salary_register_report_template.xml',
        'views/salary_register_report_template_pdf.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
}
