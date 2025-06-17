from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from database.db import get_db
import os
from datetime import datetime

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

# Decorator to check if user is a customer
def customer_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_customer:
            flash('Access denied. Customer privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@customer_bp.route('/dashboard')
@customer_required
def dashboard():
    db = get_db()
    
    # Get user's events
    events = db.fetch_all("""
        SELECT e.*, v.name as venue_name 
        FROM events e
        LEFT JOIN venues v ON e.venue_id = v.venue_id
        WHERE e.user_id = %s
        ORDER BY e.event_date DESC
    """, (current_user.id,))
    
    # Get upcoming events
    upcoming_events = db.fetch_all("""
        SELECT e.*, v.name as venue_name 
        FROM events e
        LEFT JOIN venues v ON e.venue_id = v.venue_id
        WHERE e.user_id = %s AND e.event_date >= CURDATE() AND e.status != 'cancelled'
        ORDER BY e.event_date ASC
        LIMIT 5
    """, (current_user.id,))
    
    return render_template('customer/dashboard.html', 
                           events=events, 
                           upcoming_events=upcoming_events)

@customer_bp.route('/bookings')
@customer_required
def bookings():
    db = get_db()
    
    # Get all user's events
    events = db.fetch_all("""
        SELECT e.*, v.name as venue_name 
        FROM events e
        LEFT JOIN venues v ON e.venue_id = v.venue_id
        WHERE e.user_id = %s
        ORDER BY e.event_date DESC
    """, (current_user.id,))
    
    return render_template('customer/bookings.html', events=events)

@customer_bp.route('/booking/<int:booking_id>')
@customer_required
def booking_detail(booking_id):
    db = get_db()
    
    # Get the event details
    booking = db.fetch_one("""
        SELECT e.*, v.name as venue_name, v.address as venue_address, v.description as venue_description
        FROM events e
        LEFT JOIN venues v ON e.venue_id = v.venue_id
        WHERE e.event_id = %s AND e.user_id = %s
    """, (booking_id, current_user.id))
    
    if not booking:
        flash('Booking not found or you do not have permission to view it.', 'danger')
        return redirect(url_for('customer.bookings'))
    
    # Get services for this event
    services = db.fetch_all("""
        SELECT s.name, s.description, es.quantity, es.price
        FROM event_services es
        JOIN services s ON es.service_id = s.service_id
        WHERE es.event_id = %s
    """, (booking_id,))
    
    return render_template('customer/booking_detail.html', booking=booking, services=services)

@customer_bp.route('/booking/<int:booking_id>/cancel', methods=['POST'])
@customer_required
def cancel_booking(booking_id):
    db = get_db()
    
    # Check if the booking exists and belongs to the current user
    booking = db.fetch_one("""
        SELECT * FROM events 
        WHERE event_id = %s AND user_id = %s AND status != 'cancelled'
    """, (booking_id, current_user.id))
    
    if not booking:
        flash('Booking not found, already cancelled, or you do not have permission to cancel it.', 'danger')
        return redirect(url_for('customer.bookings'))
    
    # Update the booking status to cancelled
    result = db.execute_query("""
        UPDATE events 
        SET status = 'cancelled', updated_at = NOW() 
        WHERE event_id = %s
    """, (booking_id,))
    
    if result:
        flash('Your booking has been cancelled successfully.', 'success')
    else:
        flash('Failed to cancel booking. Please try again.', 'danger')
    
    return redirect(url_for('customer.bookings'))

@customer_bp.route('/book-event', methods=['GET', 'POST'])
@customer_required
def book_event():
    db = get_db()
    
    # Get all venues
    venues = db.fetch_all("SELECT * FROM venues WHERE is_active = TRUE ORDER BY name")
    
    # Get all services
    services = db.fetch_all("SELECT * FROM services WHERE is_active = TRUE ORDER BY name")
    
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        event_type = request.form.get('event_type')
        venue_id = request.form.get('venue_id')
        event_date = request.form.get('event_date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        guest_count = request.form.get('guest_count')
        service_ids = request.form.getlist('services')
        
        # Calculate total amount (simplified version)
        total_amount = 0
        
        # Add venue cost if selected
        if venue_id:
            venue = db.fetch_one("SELECT price_per_day FROM venues WHERE venue_id = %s", (venue_id,))
            if venue and venue['price_per_day']:
                total_amount += float(venue['price_per_day'])
        
        # Add service costs
        for service_id in service_ids:
            service = db.fetch_one("SELECT price FROM services WHERE service_id = %s", (service_id,))
            if service and service['price']:
                total_amount += float(service['price'])
        
        # Create event
        event_query = """
            INSERT INTO events (user_id, venue_id, event_name, event_type, event_date, 
                               start_time, end_time, guest_count, total_amount, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending')
        """
        event_params = (current_user.id, venue_id, event_name, event_type, event_date, 
                       start_time, end_time, guest_count, total_amount)
        
        event_id = db.execute_and_get_id(event_query, event_params)
        
        if event_id:
            # Add services to event
            for service_id in service_ids:
                service = db.fetch_one("SELECT price FROM services WHERE service_id = %s", (service_id,))
                if service:
                    db.execute_query("""
                        INSERT INTO event_services (event_id, service_id, quantity, price)
                        VALUES (%s, %s, %s, %s)
                    """, (event_id, service_id, 1, service['price']))
            
            flash('Your event booking has been submitted successfully!', 'success')
            return redirect(url_for('customer.bookings'))
        
        flash('Failed to book event. Please try again.', 'danger')
    
    return render_template('customer/book_event.html', venues=venues, services=services)
