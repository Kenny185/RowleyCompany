from io import BytesIO
from flask import Blueprint, make_response, jsonify
from flask_login import login_required
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from .models import Booking, Payment, User
from reportlab.platypus.tables import Table

reports = Blueprint('reports', __name__)


@reports.route('/reports/clients')
@login_required
def clients_report():
    clients = User.query.filter_by(role='client').all()
    clients_data = [{'Surname': client.surname, 'First_name': client.first_name,
                     'Second_name': client.second_name, 'Telephone': client.telephone, 'Email': client.email
                     } for client in clients]
    return jsonify(clients_data)
    

@reports.route('/reports/booking')
@login_required
def booking_report():
    bookings = Booking.query.all()
    bookings_data = [{ 'Username': booking.username, 'Email': booking.email, 
                      'Telephone': booking.telephone,  'Property_type': booking.property_type, 
                      'Booking_hours': booking.booking_hours, 'Date': booking.date.strftime('%d/%m/%Y')
    }for booking in bookings]
    return jsonify(bookings_data)    
      
@reports.route('/reports/payments')
@login_required
def payment_report():
    payments = Payment.query.all()
    payment_data = [{'Full_name': payment.full_name, 'Id_number': payment.id_number, 
                     'Service_type': payment.service_type,  'Mpesa_number': payment.mpesa_number 
    } for payment in payments]
    return jsonify(payment_data)

@reports.route('/reports/generate_pdf/<report_type>')
def generate_pdf(report_type):
    report_data_functions = {
        'clients': (lambda: User.query.filter_by(role='client').all(), ['Surname', 'First_name', 'Second_name', 'Telephone', 'Email']),
        'bookings': (lambda: Booking.query.all(), ['Username', 'Email', 'Telephone', 'Property_type', 'Booking_hours', 'Date']),
        'payments': (lambda: Payment.query.all(), ['Full_name', 'Id_number', 'Service_type', 'Mpesa_number']),
    }
    if report_type not in report_data_functions:
        return "Invalid report type"
    
    data, headers = report_data_functions[report_type]
    
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    logo_path = 'project/static/images/de30038bf36a1146441892552da72a4e.jpg'
    logo = Image(logo_path, width=50, height=50)
    rowley_company_text = Paragraph("<b>Rowley Company</b>", ParagraphStyle(name='RowleyTextStyle', fontSize=15, alignment=1))
    logo_and_text = [[logo, Spacer(0, 1), rowley_company_text]]
    logo_and_text_table = Table(logo_and_text, colWidths=[100, None, None], style=[('ALIGN', (0, 0), (-1, -1), 'CENTRE')])

    elements.append(logo_and_text_table)
        
        
    title_style = getSampleStyleSheet()["Title"]
    title_text = f"{report_type.capitalize()} Report"
    elements.append(Spacer(1, 20)) 
    elements.append(Paragraph(title_text, title_style))

    elements.append(Spacer(1, 20)) 
    
    table_heading_style = [('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ('LEFTPADDING', (0, 0), (-1, -1), 10),
                           ('RIGHTPADDING', (0, 0), (-1, -1), 10), 
                           ('TOPPADDING', (0, 0), (-1, -1), 10), 
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 10)]

    # Create style for table rows
    table_row_style = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                       ('LEFTPADDING', (0, 0), (-1, -1), 10),
                       ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                       ('TOPPADDING', (0, 0), (-1, -1), 10), 
                       ('BOTTOMPADDING', (0, 0), (-1, -1), 10)]
    data_rows = []
    for item in data():
        data_rows.append([str(getattr(item, header.lower(), '')) for header in headers])
        
    table_data = [headers] + data_rows
    table = Table(table_data, style=table_heading_style + table_row_style, hAlign='CENTRE')
    elements.append(table)

    pdf.build(elements)
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={report_type}_report.pdf'

    return response

    