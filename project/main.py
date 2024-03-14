from flask import Blueprint, render_template
from flask_login import login_required, current_user 
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@main.route('/agent_dashboard')
@login_required
def agentDashboard():
    return render_template('agentDashboard.html', active_page='agentDashboard')

@main.route('/rowleycompany')
@login_required
def landingpage():
    return render_template('landingpage.html', active_page='landingpage')

@main.route('/booking')
@login_required
def booking():
    return render_template('booking.html', active_page='booking')

@main.route('/about')
def about():
    return render_template('about.html', active_page='about')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', active_page='profile')




