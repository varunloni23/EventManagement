from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('customer.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        db = get_db()
        user_data = db.fetch_one("SELECT * FROM users WHERE username = %s OR email = %s", (username, username))
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user, remember=remember)
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('customer.dashboard'))
        
        flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone', '')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('auth/register.html')
        
        db = get_db()
        
        # Check if username already exists
        existing_user = db.fetch_one("SELECT * FROM users WHERE username = %s", (username,))
        if existing_user:
            flash('Username already exists', 'danger')
            return render_template('auth/register.html')
        
        # Check if email already exists
        existing_email = db.fetch_one("SELECT * FROM users WHERE email = %s", (email,))
        if existing_email:
            flash('Email already exists', 'danger')
            return render_template('auth/register.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        query = """
            INSERT INTO users (username, email, password, first_name, last_name, phone, role)
            VALUES (%s, %s, %s, %s, %s, %s, 'customer')
        """
        params = (username, email, hashed_password, first_name, last_name, phone)
        
        user_id = db.execute_and_get_id(query, params)
        
        if user_id:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        
        flash('Registration failed. Please try again.', 'danger')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        db = get_db()
        
        # Check if email already exists (if changed)
        if email != current_user.email:
            existing_email = db.fetch_one("SELECT * FROM users WHERE email = %s AND user_id != %s", 
                                         (email, current_user.id))
            if existing_email:
                flash('Email already exists', 'danger')
                return redirect(url_for('auth.profile'))
        
        # Update user information
        query = """
            UPDATE users 
            SET first_name = %s, last_name = %s, email = %s, phone = %s
            WHERE user_id = %s
        """
        params = (first_name, last_name, email, phone, current_user.id)
        db.execute_query(query, params)
        
        # Update password if provided
        if current_password and new_password and confirm_password:
            if new_password != confirm_password:
                flash('New passwords do not match', 'danger')
                return redirect(url_for('auth.profile'))
            
            # Verify current password
            user_data = db.fetch_one("SELECT * FROM users WHERE user_id = %s", (current_user.id,))
            if not check_password_hash(user_data['password'], current_password):
                flash('Current password is incorrect', 'danger')
                return redirect(url_for('auth.profile'))
            
            # Update password
            hashed_password = generate_password_hash(new_password)
            db.execute_query("UPDATE users SET password = %s WHERE user_id = %s", 
                           (hashed_password, current_user.id))
            flash('Password updated successfully', 'success')
        
        flash('Profile updated successfully', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html')
