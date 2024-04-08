from flask import Blueprint, flash, get_flashed_messages, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from . import db
from project.models import Booking, Payment, User
from datetime import datetime

client = Blueprint('client',  __name__)

@client.route('/profile', methods=['POST'])
@login_required
def update_profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if user:
        user.surname = request.form['surname']
        user.first_name = request.form['first_name']
        user.second_name = request.form['second_name']
        user.telephone = request.form['telephone']
        user.email = request.form['email']
        # user.password = request.form['password']
        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
            
        return redirect(url_for('main.profile', user_id=user_id))
 
@client.route('/booking', methods=['POST'])
@login_required
def booking_post():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        telephone = request.form['telephone']
        property_type = request.form['property-type']
        booking_hours = request.form['booking-hours']
        
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%d/%m/%Y').date()
        
        new_booking = Booking(username=username, email=email, telephone=telephone,
                              property_type=property_type, booking_hours=booking_hours, date=date,
                              user_id=current_user.id)
        
        db.session.add(new_booking)
        db.session.commit()
        
        flash('Your booking has been successful!', 'success')
        return redirect(url_for('main.clientDashboard'))
        
    return render_template('booking.html') 

@client.route('/payment', methods=['POST'])
@login_required
def payment_post():
    full_name = request.form['full_name']
    id_number = request.form['id_number']
    service_type = request.form['service-type']
    mpesa_number = request.form['mpesa_number']
    
    new_payment = Payment(full_name=full_name, id_number=id_number, 
                          service_type=service_type, mpesa_number=mpesa_number,
                          user_id=current_user.id)
    db.session.add(new_payment)
    db.session.commit()
    
    flash('Your payment has been successful', 'success')    
    return redirect(url_for('main.clientDashboard')) 

@client.route('/client/proceed_to_payment/<int:booking_id>')
@login_required
def proceed_to_payment(booking_id):
    booking = Booking.query.filter_by(id=booking_id, user_id=current_user.id).first_or_404()
    return render_template('payment.html', booking=booking)

@client.route('/booking/modify/<int:booking_id>', methods=['POST'])
@login_required
def modify_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('You are not authorized to modify this booking.', 'danger')
        return redirect(url_for('main.clientDashboard'))

    # Update booking details
    booking.username = request.form['username']
    booking.email = request.form['email']
    booking.telephone = request.form['telephone']
    booking.property_type = request.form['property-type']
    booking.booking_hours = request.form['booking-hours']
    
    date_str = request.form['date']
    booking.date = datetime.strptime(date_str, '%d/%m/%Y').date()

    db.session.commit()
    flash('Booking modified successfully.', 'success')
    print("Flash Messages:", get_flashed_messages(with_categories=True))

    return redirect(url_for('main.clientDashboard'))

@client.route('/booking/delete/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash("You're not authorized to delete this booking.", 'danger')
        return redirect(url_for('main.clientDashboard'))
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted successfully.', 'success')
    return redirect(url_for('main.clientDashboard'))


@client.route('/booking/history',  methods=['GET'])
@login_required
def bookingHistory():
    property_type = request.args.get('property_type', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    bookings_query = Booking.query.filter_by(user_id=current_user.id)

    if property_type:
        bookings_query = bookings_query.filter(Booking.property_type.ilike(f'%{property_type}%'))
    if start_date:
        start_date_obj = datetime.strptime(start_date, '%d/%m/%Y').date()
        bookings_query = bookings_query.filter(Booking.date >= start_date_obj)
    if end_date:
        end_date_obj = datetime.strptime(end_date, '%d/%m/%Y').date()
        bookings_query = bookings_query.filter(Booking.date <= end_date_obj)

    bookings = bookings_query.all()   
    return render_template('bookingHistory.html', active_page='bookingHistory',  bookings=bookings)
