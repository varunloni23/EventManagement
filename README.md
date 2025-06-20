# Event Management System

A comprehensive event management system built with Flask and MySQL, designed for event planning companies to manage their services, venues, and customer bookings.

## Features

- **User Authentication**: Separate login systems for customers and administrators
- **Customer Portal**: Browse services and venues, book events, view booking history, submit testimonials
- **Admin Dashboard**: Manage services, venues, events, testimonials, and blog posts
- **Service Management**: Add, edit, and categorize different event services
- **Venue Management**: Manage event venues with details and availability
- **Event Booking**: Complete event booking system with service selection
- **Blog System**: Create and manage blog posts
- **Gallery**: Upload and showcase event photos and videos
- **Testimonials**: Customer reviews and feedback system
- **Responsive Design**: Mobile-friendly interface

## Technology Stack

- **Backend**: Python, Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login
- **Form Handling**: Flask-WTF
- **File Uploads**: Werkzeug

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/event-management.git
   cd event-management
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the MySQL database:
   ```
   mysql -u root -p < database/event_management.sql
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Access the application at `http://localhost:5000`

## Configuration

- Database configuration can be modified in `database/db.py`
- Application settings can be adjusted in `app.py`

## Default Admin Credentials

- Username: admin
- Password: admin123

## Project Structure

```
event-management/
├── app.py                  # Main application file
├── database/               # Database related files
│   ├── db.py               # Database connection module
│   └── event_management.sql # SQL schema
├── models/                 # Data models
│   ├── __init__.py
│   └── user.py             # User model
├── routes/                 # Route handlers
│   ├── __init__.py
│   ├── admin_routes.py     # Admin routes
│   ├── auth_routes.py      # Authentication routes
│   ├── common_routes.py    # Common routes
│   └── customer_routes.py  # Customer routes
├── static/                 # Static files
│   ├── css/                # CSS files
│   ├── js/                 # JavaScript files
│   └── images/             # Image files
└── templates/              # HTML templates
    ├── admin/              # Admin templates
    ├── auth/               # Authentication templates
    ├── customer/           # Customer templates
    ├── errors/             # Error page templates
    └── base.html           # Base template
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bootstrap for the responsive design components
- Font Awesome for the icons
- Google Fonts for the typography # EventManagement
# EventManagemnt
