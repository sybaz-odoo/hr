from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo import models, fields, api

class SalaryRegisterWizard(models.TransientModel):
    _name = 'salary.register.report.wizard'
    _description = 'Salary Register Report Wizard'

    month = fields.Selection([
        ('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
        ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
        ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December'),
    ], string='Month', required=True)

    year = fields.Selection(
        selection=lambda self: self._get_year_selection(),
        string='Year',
        required=True
    )

    @api.model
    def _get_year_selection(self):
        # Collect years from hr.payslip.date_from
        payslip_dates = self.env['hr.payslip'].search([]).mapped('date_from')
        unique_years = sorted({str(date.year) for date in payslip_dates if date})
        return [(y, y) for y in unique_years]

    def generate_report_htm(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        report_url = f"{base_url}/web/salary_register_report?month={self.month}&year={self.year}" \
                     f"&display_type=htm"

        return {
            'type': 'ir.actions.act_url',
            'url': report_url,
            'target': 'new'
        }
