from flask import Blueprint, render_template, request
from flask_login import login_required, current_user 
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/home')
def home():
    return render_template('home.html', active_page='home')

@main.route('/client_dashboard')
@login_required
def clientDashboard():
    return render_template('clientDashboard.html', active_page='clientDashboard')

@main.route('/agent_dashboard')
@login_required
def agentDashboard():
    return render_template('agentDashboard.html', active_page='agentDashboard')

@main.route('/rowleycompany')
@login_required
def landingpage():
    return render_template('landingpage.html', active_page='landingpage')


@main.route('/about')
def about():
    return render_template('about.html', active_page='about')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', active_page='profile')

@main.route('/booking')
@login_required
def booking():
    return render_template('booking.html', active_page='booking')

@main.route('/payment')
@login_required
def payment():
    username = request.args.get('username')
    email = request.args.get('email')
    telephone = request.args.get('telephone')
    property_type = request.args.get('property_type')
    booking_hours = request.args.get('booking_hours')
    date = request.args.get('date')
    return render_template('payment.html', active_page='payment', username=username, 
                           email=email, telephone=telephone, property_type=property_type, 
                           booking_hours=booking_hours, date=date)


