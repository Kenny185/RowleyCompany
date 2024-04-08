from flask import Blueprint, flash, redirect, url_for
from project.models import Booking, User
from . import db


agent = Blueprint('agent',  __name__)

@agent.route('/agent/accept_booking/<int:booking_id>', methods=['POST'])
def accept_booking(booking_id):
    # Find the booking by ID
    booking = Booking.query.get_or_404(booking_id)
    # Update booking status to accepted
    booking.status = 'Accepted'
    db.session.commit()
    
    flash('Booking accepted successfully!', 'success')
    return redirect(url_for('main.agentDashboard'))

@agent.route('/agent/assign_agent/<int:booking_id>/<int:agent_id>', methods=['POST'])
def assign_agent(booking_id, agent_id):
    # Find the booking by ID
    booking = Booking.query.get_or_404(booking_id)
    # Find the agent by ID
    agent = User.query.get_or_404(agent_id)
    # Update booking with assigned agent
    booking.agent = agent
    db.session.commit()
    flash('Agent assigned to booking!', 'success')
    # Send confirmation message to client
    send_confirmation_message(booking, agent)
    return redirect(url_for('main.agentDashboard'))

def send_confirmation_message(booking, agent):
    # Logic to send confirmation message to client
    pass