from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from database.db import get_db
from datetime import datetime

common_bp = Blueprint('common', __name__)

@common_bp.route('/about')
def about():
    return render_template('about.html')

@common_bp.route('/services')
def services():
    db = get_db()
    
    # Get service categories with their services
    categories = db.fetch_all("SELECT * FROM service_categories ORDER BY name")
    
    services_by_category = {}
    for category in categories:
        category_id = category['category_id']
        services = db.fetch_all("""
            SELECT s.* FROM services s
            JOIN service_category_mapping scm ON s.service_id = scm.service_id
            WHERE scm.category_id = %s AND s.is_active = TRUE
            ORDER BY s.name
        """, (category_id,))
        services_by_category[category_id] = services
    
    return render_template('services.html', 
                           categories=categories, 
                           services_by_category=services_by_category)

@common_bp.route('/service/<int:service_id>')
def service_detail(service_id):
    db = get_db()
    
    # Get service details
    service = db.fetch_one("""
        SELECT s.*, c.name as category_name, c.category_id
        FROM services s
        JOIN service_category_mapping scm ON s.service_id = scm.service_id
        JOIN service_categories c ON scm.category_id = c.category_id
        WHERE s.service_id = %s AND s.is_active = TRUE
    """, (service_id,))
    
    if not service:
        flash('Service not found', 'danger')
        return redirect(url_for('common.services'))
    
    # Get related services in same category
    related_services = db.fetch_all("""
        SELECT s.* FROM services s
        JOIN service_category_mapping scm ON s.service_id = scm.service_id
        WHERE scm.category_id = %s AND s.service_id != %s AND s.is_active = TRUE
        LIMIT 3
    """, (service['category_id'], service_id))
    
    return render_template('service_detail.html', 
                           service=service, 
                           related_services=related_services)

@common_bp.route('/venues')
def venues():
    db = get_db()
    venues = db.fetch_all("SELECT * FROM venues WHERE is_active = TRUE ORDER BY name")
    return render_template('venues.html', venues=venues)

@common_bp.route('/venue/<int:venue_id>')
def venue_detail(venue_id):
    db = get_db()
    
    # Get venue details
    venue = db.fetch_one("SELECT * FROM venues WHERE venue_id = %s AND is_active = TRUE", (venue_id,))
    
    if not venue:
        flash('Venue not found', 'danger')
        return redirect(url_for('common.venues'))
    
    # Get gallery items for this venue
    gallery_items = db.fetch_all("""
        SELECT g.* FROM gallery g
        JOIN events e ON g.event_id = e.event_id
        WHERE e.venue_id = %s
        LIMIT 6
    """, (venue_id,))
    
    return render_template('venue_detail.html', venue=venue, gallery_items=gallery_items)

@common_bp.route('/gallery')
def gallery():
    db = get_db()
    
    # Get gallery items by type
    photos = db.fetch_all("SELECT * FROM gallery WHERE type = 'photo' ORDER BY created_at DESC LIMIT 12")
    videos = db.fetch_all("SELECT * FROM gallery WHERE type = 'video' ORDER BY created_at DESC LIMIT 6")
    shorts = db.fetch_all("SELECT * FROM gallery WHERE type = 'short' ORDER BY created_at DESC LIMIT 6")
    albums = db.fetch_all("SELECT * FROM gallery WHERE type = 'album' ORDER BY created_at DESC LIMIT 6")
    
    return render_template('gallery.html', 
                           photos=photos, 
                           videos=videos, 
                           shorts=shorts, 
                           albums=albums)

@common_bp.route('/blog')
def blog():
    db = get_db()
    blogs = db.fetch_all("""
        SELECT b.*, u.first_name, u.last_name
        FROM blog_posts b
        JOIN users u ON b.author_id = u.user_id
        WHERE b.is_published = TRUE
        ORDER BY b.published_at DESC
    """)
    return render_template('blog.html', blogs=blogs)

@common_bp.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    db = get_db()
    
    # Get blog details
    blog = db.fetch_one("""
        SELECT b.*, u.first_name, u.last_name
        FROM blog_posts b
        JOIN users u ON b.author_id = u.user_id
        WHERE b.post_id = %s AND b.is_published = TRUE
    """, (blog_id,))
    
    if not blog:
        flash('Blog post not found', 'danger')
        return redirect(url_for('common.blog'))
    
    # Get related blog posts
    related_blogs = db.fetch_all("""
        SELECT b.*, u.first_name, u.last_name
        FROM blog_posts b
        JOIN users u ON b.author_id = u.user_id
        WHERE b.post_id != %s AND b.is_published = TRUE
        ORDER BY b.published_at DESC
        LIMIT 3
    """, (blog_id,))
    
    return render_template('blog_detail.html', blog=blog, related_blogs=related_blogs)

@common_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        db = get_db()
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        message = request.form.get('message')
        
        # Add contact message
        db.execute_query(
            "INSERT INTO contact_messages (name, email, phone, message) VALUES (%s, %s, %s, %s)",
            (name, email, phone, message)
        )
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('common.contact'))
    
    return render_template('contact.html')

@common_bp.route('/testimonials')
def testimonials():
    db = get_db()
    testimonials = db.fetch_all("""
        SELECT t.*, u.first_name, u.last_name
        FROM testimonials t
        JOIN users u ON t.user_id = u.user_id
        WHERE t.is_approved = TRUE
        ORDER BY t.created_at DESC
    """)
    return render_template('testimonials.html', testimonials=testimonials) 