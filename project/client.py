import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from . import db
from project.models import Booking, Payment, User

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
        date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
        date = date_obj.strftime('%Y-%m-%d')
        
        new_booking = Booking(username=username, email=email, telephone=telephone,
                              property_type=property_type, booking_hours=booking_hours, date=date,
                              user_id=current_user.id)
        
        db.session.add(new_booking)
        db.session.commit()
        
        flash('Your booking has been successful! <a href="' + url_for('main.clientDashboard') + '"> Click to Return to Dashboard </a>', 'success')
        
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

@client.route('/proceed_to_payment/<int:booking_id>')
@login_required
def proceed_to_payment(booking_id):
    booking = Booking.query.filter_by(id=booking_id, user_id=current_user.id).first_or_404()
    return render_template('payment.html', booking=booking)

@client.route('/modify_booking/<int:booking_id>', methods=['POST'])
@login_required
def modify_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('You are not authorized to modify this booking.', 'error')
        return redirect(url_for('main.clientDashboard'))

    # Update booking details
    booking.property_type = request.form['property_type']
    booking.date = request.form['date']
    # Add other fields as necessary

    db.session.commit()
    flash('Booking modified successfully.', 'success')
    return redirect(url_for('main.clientDashboard'))

@client.route('/delete_booking/<int:booking_id>', methods=['POST'])
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


@client.route('/booking_history',  methods=['GET'])
@login_required
def bookingHistory():
    property_type = request.args.get('property_type', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    bookings_query = Booking.query.filter_by(user_id=current_user.id)

    if property_type:
        bookings_query = bookings_query.filter(Booking.property_type.ilike(f'%{property_type}%'))
    if start_date:
        start_date_obj = datetime.datetime.strptime(start_date, '%d/%m/%Y').date()
        bookings_query = bookings_query.filter(Booking.date >= start_date_obj.strftime('%Y-%m-%d'))
    if end_date:
        end_date_obj = datetime.datetime.strptime(end_date, '%d/%m/%Y').date()
        bookings_query = bookings_query.filter(Booking.date <= end_date_obj.strftime('%Y-%m-%d'))

    bookings = bookings_query.all()   
    return render_template('bookingHistory.html', active_page='payment',  bookings=bookings)

