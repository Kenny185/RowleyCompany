from io import BytesIO
from flask import Blueprint, make_response, jsonify
from flask_login import login_required
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Booking, Payment, User
from . import db

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
                      'Booking_hours': booking.booking_hours, 'Date': booking.date
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
    pdf = canvas.Canvas(buffer, pagesize=letter)
    def header(canvas, report_type):
        canvas.saveState()
        canvas.drawImage('/static/images/logo.jpeg', 50, 750, width=100, height=50)
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(100, 750, f"{report_type.capitalize()} Report")
        canvas.restoreState()
        
    pdf._header = lambda canvas, report_type: header(canvas, report_type)
    
    row_height = 720
    for header in headers:
        pdf.drawString(headers.index(header) * 200 + 50, row_height, header)
    row_height -= 20

    for item in data():
        if report_type == 'clients':
            pdf.drawString(50, row_height, item.surname)
            pdf.drawString(250, row_height, item.first_name)
            pdf.drawString(450, row_height, item.second_name)
            pdf.drawString(650, row_height, item.telephone)
            pdf.drawString(850, row_height, item.email)
        elif report_type == 'bookings':
            pdf.drawString(50, row_height, item.user.username)
            pdf.drawString(250, row_height, item.service.email)
            pdf.drawString(450, row_height, item.service.telephone)
            pdf.drawString(650, row_height, item.service.property_type)
            pdf.drawString(850, row_height, item.service.booking_hours)
            pdf.drawString(1050, row_height, item.service.date)
        elif report_type == 'payments':
            pdf.drawString(50, row_height, item.full_name)
            pdf.drawString(250, row_height, item.id_number)
            pdf.drawString(450, row_height, item.service_type)
            pdf.drawString(650, row_height, item.mpesa_number)
        row_height -= 20

    pdf.save()
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={report_type}_report.pdf'

    return response

    