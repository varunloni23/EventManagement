from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import json

# Import database connection
from database.db import get_db, close_db

# Create Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    db = get_db()
    user_data = db.fetch_one("SELECT * FROM users WHERE user_id = %s", (user_id,))
    if user_data:
        return User(user_data)
    return None

# Register teardown to close database connection
@app.teardown_appcontext
def teardown_db(exception):
    close_db()

# Add context processor for current year
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Import routes after app is created to avoid circular imports
from routes.auth_routes import auth_bp
from routes.customer_routes import customer_bp
from routes.admin_routes import admin_bp
from routes.common_routes import common_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(common_bp)

# Home route
@app.route('/')
def index():
    db = get_db()
    
    # Get services
    services = db.fetch_all("""
        SELECT s.*, c.name as category_name 
        FROM services s
        JOIN service_category_mapping scm ON s.service_id = scm.service_id
        JOIN service_categories c ON scm.category_id = c.category_id
        WHERE s.is_active = TRUE
        LIMIT 8
    """)
    
    # Get venues
    venues = db.fetch_all("SELECT * FROM venues WHERE is_active = TRUE LIMIT 8")
    
    # Get testimonials
    testimonials = db.fetch_all("""
        SELECT t.*, u.first_name, u.last_name 
        FROM testimonials t
        JOIN users u ON t.user_id = u.user_id
        WHERE t.is_approved = TRUE
        ORDER BY t.created_at DESC
        LIMIT 5
    """)
    
    # Get blog posts
    blog_posts = db.fetch_all("""
        SELECT * FROM blog_posts 
        WHERE is_published = TRUE 
        ORDER BY published_at DESC
        LIMIT 3
    """)
    
    return render_template('index.html', 
                           services=services, 
                           venues=venues, 
                           testimonials=testimonials, 
                           blog_posts=blog_posts)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True) 