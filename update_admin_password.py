from werkzeug.security import generate_password_hash
from database.db import get_db
from app import app

def update_admin_password():
    # Connect to the database
    with app.app_context():
        db = get_db()
        
        # Generate a proper password hash
        password = 'admin123'
        hashed_password = generate_password_hash(password)
        
        # Update the admin user's password
        query = "UPDATE users SET password = %s WHERE username = 'admin'"
        result = db.execute_query(query, (hashed_password,))
        
        if result:
            print(f"Admin password updated successfully to '{password}'")
            print(f"Hash: {hashed_password}")
        else:
            print("Failed to update admin password")
    
    # Close the database connection
    db.close()

if __name__ == "__main__":
    update_admin_password() 