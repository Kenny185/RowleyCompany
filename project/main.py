import datetime
from flask import Blueprint, render_template, request, current_app
from flask_login import login_required, current_user
from itsdangerous import URLSafeSerializer
from project.models import Booking, User 
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/home')
def home():
    return render_template('home.html', active_page='home')

@main.route('/client/dashboard')
@login_required
def clientDashboard():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('clientDashboard.html', active_page='clientDashboard', bookings=bookings)

@main.route('/agent/dashboard')
@login_required
def agentDashboard():
    bookings = Booking.query.all()
    return render_template('agentDashboard.html', active_page='agentDashboard', bookings=bookings)

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
    return render_template('payment.html', active_page='payment')
