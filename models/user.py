from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['user_id']
        self.username = user_data['username']
        self.email = user_data['email']
        self.first_name = user_data['first_name']
        self.last_name = user_data['last_name']
        self.phone = user_data.get('phone', '')
        self.role = user_data['role']
        self.created_at = user_data['created_at']
        self.updated_at = user_data['updated_at']
    
    def get_id(self):
        return str(self.id)
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_customer(self):
        return self.role == 'customer'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}" 