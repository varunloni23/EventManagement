from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database.db import get_db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorator to check if user is an admin
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    db = get_db()
    
    # Get counts for dashboard
    pending_events = db.fetch_one("SELECT COUNT(*) as count FROM events WHERE status = 'pending'")
    total_events = db.fetch_one("SELECT COUNT(*) as count FROM events")
    total_customers = db.fetch_one("SELECT COUNT(*) as count FROM users WHERE role = 'customer'")
    total_revenue = db.fetch_one("SELECT SUM(total_amount) as total FROM events WHERE status != 'cancelled'")
    
    # Get recent events
    recent_events = db.fetch_all("""
        SELECT e.*, u.first_name, u.last_name, v.name as venue_name 
        FROM events e
        JOIN users u ON e.user_id = u.user_id
        LEFT JOIN venues v ON e.venue_id = v.venue_id
        ORDER BY e.created_at DESC
        LIMIT 5
    """)
    
    return render_template('admin/dashboard.html',
                           pending_events=pending_events['count'],
                           total_events=total_events['count'],
                           total_customers=total_customers['count'],
                           total_revenue=total_revenue['total'] if total_revenue['total'] else 0,
                           recent_events=recent_events)

@admin_bp.route('/events')
@admin_required
def events():
    db = get_db()
    
    # Get all events
    events = db.fetch_all("""
        SELECT e.*, u.first_name, u.last_name, v.name as venue_name 
        FROM events e
        JOIN users u ON e.user_id = u.user_id
        LEFT JOIN venues v ON e.venue_id = v.venue_id
        ORDER BY e.event_date DESC
    """)
    
    return render_template('admin/events.html', events=events)

@admin_bp.route('/events/<int:event_id>')
@admin_required
def view_event(event_id):
    db = get_db()
    
    # Get event details
    event = db.fetch_one("""
        SELECT e.*, u.first_name, u.last_name, u.email, u.phone, v.name as venue_name, v.address as venue_address
        FROM events e
        JOIN users u ON e.user_id = u.user_id
        LEFT JOIN venues v ON e.venue_id = v.venue_id
        WHERE e.event_id = %s
    """, (event_id,))
    
    if not event:
        flash('Event not found', 'danger')
        return redirect(url_for('admin.events'))
    
    # Get services for this event
    services = db.fetch_all("""
        SELECT s.name, s.description, es.quantity, es.price
        FROM event_services es
        JOIN services s ON es.service_id = s.service_id
        WHERE es.event_id = %s
    """, (event_id,))
    
    return render_template('admin/view_event.html', event=event, services=services)

@admin_bp.route('/testimonials')
@admin_required
def testimonials():
    db = get_db()
    
    # Get all testimonials
    testimonials = db.fetch_all("""
        SELECT t.*, u.first_name, u.last_name, e.event_name
        FROM testimonials t
        JOIN users u ON t.user_id = u.user_id
        LEFT JOIN events e ON t.event_id = e.event_id
        ORDER BY t.created_at DESC
    """)
    
    return render_template('admin/testimonials.html', testimonials=testimonials)

@admin_bp.route('/testimonials/<int:testimonial_id>/approve', methods=['POST'])
@admin_required
def approve_testimonial(testimonial_id):
    db = get_db()
    
    # Update testimonial to approved
    result = db.execute_query("""
        UPDATE testimonials
        SET is_approved = TRUE
        WHERE testimonial_id = %s
    """, (testimonial_id,))
    
    if result:
        flash('Testimonial approved successfully', 'success')
    else:
        flash('Failed to approve testimonial', 'danger')
    
    return redirect(url_for('admin.testimonials'))

@admin_bp.route('/testimonials/<int:testimonial_id>/delete', methods=['POST'])
@admin_required
def delete_testimonial(testimonial_id):
    db = get_db()
    
    # Delete testimonial
    result = db.execute_query("""
        DELETE FROM testimonials
        WHERE testimonial_id = %s
    """, (testimonial_id,))
    
    if result:
        flash('Testimonial deleted successfully', 'success')
    else:
        flash('Failed to delete testimonial', 'danger')
    
    return redirect(url_for('admin.testimonials'))

@admin_bp.route('/messages')
@admin_required
def messages():
    db = get_db()
    
    # Get all messages
    messages = db.fetch_all("""
        SELECT *
        FROM contact_messages
        ORDER BY created_at DESC
    """)
    
    return render_template('admin/messages.html', messages=messages)

@admin_bp.route('/messages/<int:message_id>')
@admin_required
def view_message(message_id):
    db = get_db()
    
    # Get message details
    message = db.fetch_one("""
        SELECT *
        FROM contact_messages
        WHERE message_id = %s
    """, (message_id,))
    
    if not message:
        flash('Message not found', 'danger')
        return redirect(url_for('admin.messages'))
    
    # Mark message as read
    if not message['is_read']:
        db.execute_query("""
            UPDATE contact_messages
            SET is_read = TRUE
            WHERE message_id = %s
        """, (message_id,))
    
    return render_template('admin/view_message.html', message=message)

@admin_bp.route('/events/<int:event_id>/status/<status>', methods=['POST'])
@admin_required
def update_event_status(event_id, status):
    if status not in ['pending', 'confirmed', 'cancelled', 'completed']:
        flash('Invalid status', 'danger')
        return redirect(url_for('admin.events'))
    
    db = get_db()
    
    # Update event status
    result = db.execute_query("""
        UPDATE events
        SET status = %s, updated_at = NOW()
        WHERE event_id = %s
    """, (status, event_id))
    
    if result:
        flash(f'Event status updated to {status}', 'success')
    else:
        flash('Failed to update event status', 'danger')
    
    return redirect(url_for('admin.events'))

@admin_bp.route('/messages/<int:message_id>/delete', methods=['POST'])
@admin_required
def delete_message(message_id):
    db = get_db()
    
    # Delete message
    result = db.execute_query("""
        DELETE FROM contact_messages
        WHERE message_id = %s
    """, (message_id,))
    
    if result:
        flash('Message deleted successfully', 'success')
    else:
        flash('Failed to delete message', 'danger')
    
    return redirect(url_for('admin.messages'))
