from flask import Blueprint, flash, redirect, url_for
from flask_login import current_user
from project.models import Booking, User
from datetime import datetime
from . import db


agent = Blueprint('agent',  __name__)

@agent.route('/agent/booking/accept/<int:booking_id>', methods=['POST'])
def accept_booking(booking_id):
    # Find the booking by ID
    booking = Booking.query.get_or_404(booking_id)
    # Check if there are fewer than five bookings for the given date
    date_of_booking = booking.date
    bookings_for_date = Booking.query.filter_by(date=date_of_booking).count() 
    if bookings_for_date >= 5:
        flash('Sorry, there are already five bookings for this day. Cannot accept new booking.', 'danger')
        return redirect(url_for('main.agentDashboard'))
    # Update booking status to accepted
    booking.status = 'Accepted'
    db.session.commit()
    
    flash('Booking accepted successfully!', 'success')
    return redirect(url_for('main.agentDashboard'))

@agent.route('/agent/assign_agent/<int:booking_id>/<int:agent_id>', methods=['POST'])
def assign_agent(booking_id, agent_id):
    # Find the booking by ID
    booking = Booking.query.get_or_404(booking_id)
    if booking.status == 'Accepted':
        booking.status = 'Assigned'
        booking.agent_id = agent_id  # Use the agent_id passed from the URL
        db.session.commit()
        flash('Agent assigned to booking!', 'success')
    
    return redirect(url_for('main.agentDashboard'))
