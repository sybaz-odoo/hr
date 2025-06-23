import calendar

from odoo import http
from odoo.http import request
import xlsxwriter
from io import BytesIO
from datetime import datetime


class SalaryRegisterReportController(http.Controller):
    @http.route('/web/salary_register_report', type="http", auth="user", website=True, csrf=False)
    def salary_register_report(self, month, year, display_type, **kwargs):
        month = int(month)
        year = int(year)
        # First day of the month
        start_date = datetime(year, month, 1).date()

        # Last day of the month
        last_day = calendar.monthrange(year, month)[1]
        end_date = datetime(year, month, last_day).date()

        data = self._get_data(start_date, end_date)
        month_name = calendar.month_name[int(month)]
        disp_month_year = "For the month of " + month_name + " " + str(year)

        if display_type == 'htm':
            return request.render('sb_salary_register.salary_register_report_template', {
                'data': data,
                'month': month,
                'year': year,
                'disp_month_year': disp_month_year,
                'company_name': request.env.user.company_id.name
            })
        elif display_type == 'xls':
            file_content = self._create_excel_file(data, disp_month_year)
            file_name = f"salary_register_report.xlsx"

            return request.make_response(
                file_content,
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    ('Content-Disposition', f'attachment; filename={file_name}')
                ]
            )
        else:
            datas = {
                'det_data': data, 'disp_month_year': disp_month_year, 'company_name': request.env.user.company_id.name
            }
            pdf = \
            request.env['ir.actions.report'].sudo()._render_qweb_pdf('sb_salary_register.action_salary_register_report',
                                                                     data=datas)[0]

            pdfhttpheaders = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(pdf)),
            ]
            return request.make_response(pdf, headers=pdfhttpheaders)


    def _get_data(self, start_date, end_date):
        payslips = request.env['hr.payslip'].sudo().search([
            ('state', '=', 'done'),
            ('date_from', '>=', start_date),
            ('date_to', '<=', end_date),
        ], order='employee_id')

        report_data = []
        for slip in payslips:
            emp = slip.employee_id
            contract = slip.contract_id

            def get_line(code):
                return slip.line_ids.filtered(lambda l: l.code == code)

            def get_worked_days(name):
                return slip.worked_days_line_ids.filtered(lambda l: l.name == name)

            # Salary Lines
            emp_basic = get_line('BASIC')
            emp_hra = get_line('HRA')
            emp_ca = get_line('CA')
            salary_gross = get_line('GROSS')
            emp_pf = get_line('PF')
            emp_pt = get_line('PT')
            salary_net = get_line('NET')

            emp_basic = getattr(emp_basic, 'total', 0.0)
            emp_hra = getattr(emp_hra, 'total', 0.0)
            emp_ca = getattr(emp_ca, 'total', 0.0)
            salary_gross = getattr(salary_gross, 'total', 0.0)
            emp_pf = abs(getattr(emp_pf, 'total', 0.0))
            emp_pt = abs(getattr(emp_pt, 'total', 0.0))
            salary_net = getattr(salary_net, 'total', 0.0)

            report_data.append({
                'emp_name': emp.name,
                'emp_desg': emp.job_id.name or '',
                'emp_dept': emp.department_id.name or '',
                'emp_basic': emp_basic,
                'emp_hra': emp_hra,
                'emp_ca': emp_ca,
                'emp_pf': emp_pf,
                'emp_pt': emp_pt,
                'salary_gross': salary_gross,
                'salary_net': salary_net
            })
        report_data = sorted(report_data, key=lambda x: x['emp_name'].lower() if x['emp_name'] else '')
        return report_data

    def format_number_qty(self, balance):
        if balance < 0:
            return '({:,.4f})'.format(abs(balance))
        else:
            return '{:,.4f}'.format(balance)

    def format_number_value(self, balance):
        # Format negative values with parentheses and keep precision to 2 decimal places
        if balance < 0:
            return '({:,.2f})'.format(abs(balance))
        else:
            return '{:,.2f}'.format(balance)

    def _create_excel_file(self, data, disp_month_year):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Salary Register Report')

        decimal_format2 = workbook.add_format({'valign': 'vcenter', 'num_format': '#,##0.00;(#,##0.00)'})
        format0 = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'
        })
        format1 = workbook.add_format({
            'text_wrap': True,
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        format2 = workbook.add_format({
            'text_wrap': True,
            'bold': True,
            'align': 'right',
            'border': 1,
            'valign': 'vcenter'
        })
        format4 = workbook.add_format({
            'bold': True,
            'border': 1,
            'num_format': '#,##0.00;(#,##0.00)'
        })
        format7 = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter'
        })
        format8 = workbook.add_format({
            'text_wrap': True,
            'valign': 'vcenter'
        })
        format9 = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter'
        })
        c = 0
        worksheet.set_column(c, c, 5)
        c += 1
        worksheet.set_column(c, c, 25)
        c += 1
        worksheet.set_column(c, c, 25)
        c += 1
        worksheet.set_column(c, c, 25)
        c += 1
        worksheet.set_column(c, c, 13)
        c += 1
        worksheet.set_column(c, c, 13)
        c += 1
        worksheet.set_column(c, c, 13)
        c += 1
        worksheet.set_column(c, c, 13)
        c += 1
        worksheet.set_column(c, c, 13)
        c += 1
        worksheet.set_column(c, c, 13)
        c += 1
        worksheet.set_column(c, c, 13)

        # Get the company name
        company_name = request.env.user.company_id.name

        row = 0
        # Write the company name to the first row
        worksheet.merge_range(row, 0, row, 10, company_name, format0)

        row = row + 1
        worksheet.merge_range(row, 0, row, 10, 'Salary Register Report', format0)
        headers = ['Basic Salary', 'House Rent Allowance', 'Conveyance Allowance', 'Gross Salary',
                   'Provident Fund', 'Professional Tax', 'Net Salary']

        row = row + 1
        worksheet.merge_range(row, 0, row, 10, disp_month_year, format9)

        # Write the header starting from the second row
        row = row + 1
        worksheet.write(row, 0, 'Sr.#', format1)
        worksheet.write(row, 1, 'Employee Name', format1)
        worksheet.write(row, 2, 'Designation', format1)
        worksheet.write(row, 3, 'Department', format1)
        for col_num, header in enumerate(headers):
            worksheet.write(row, col_num + 4, header, format2)

        # Write the data
        row = row + 1
        row_num = row
        rec_no = 1
        for line in data[0:]:
            worksheet.write(row_num, 0, rec_no, format7)
            worksheet.write(row_num, 1, line['emp_name'], format8)
            worksheet.write(row_num, 2, line['emp_desg'], format8)
            worksheet.write(row_num, 3, line['emp_dept'], format8)
            cols = [
                ('emp_basic', decimal_format2),
                ('emp_hra', decimal_format2),
                ('emp_ca', decimal_format2),
                ('salary_gross', decimal_format2),
                ('emp_pf', decimal_format2),
                ('emp_pt', decimal_format2),
                ('salary_net', decimal_format2),
            ]

            for col_offset, (key, fmt) in enumerate(cols, start=4):
                worksheet.write(row_num, col_offset, line[key], fmt)

            row_num = row_num + 1
            rec_no = rec_no + 1

        gt_basic = sum(line['emp_basic'] for line in data)
        gt_hra = sum(line['emp_hra'] for line in data)
        gt_ca = sum(line['emp_ca'] for line in data)
        gt_gross = sum(line['salary_gross'] for line in data)
        gt_pf = sum(line['emp_pf'] for line in data)
        gt_pt = sum(line['emp_pt'] for line in data)
        gt_net = sum(line['salary_net'] for line in data)

        worksheet.write(row_num, 3, 'Grand Total', format4)
        worksheet.write(row_num, 4, gt_basic, format4)
        worksheet.write(row_num, 5, gt_hra, format4)
        worksheet.write(row_num, 6, gt_ca, format4)
        worksheet.write(row_num, 7, gt_gross, format4)
        worksheet.write(row_num, 8, gt_pf, format4)
        worksheet.write(row_num, 9, gt_pt, format4)
        worksheet.write(row_num, 10, gt_net, format4)

        workbook.close()
        output.seek(0)
        return output.read()
