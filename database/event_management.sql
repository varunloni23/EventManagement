-- Event Management System Database Schema

-- Drop database if exists
DROP DATABASE IF EXISTS event_management;

-- Create database
CREATE DATABASE event_management;

-- Use the database
USE event_management;

-- Users table (for both customers and admins)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    role ENUM('customer', 'admin') DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Services table
CREATE TABLE services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    image_path VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Service categories
CREATE TABLE service_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Map services to categories
CREATE TABLE service_category_mapping (
    mapping_id INT AUTO_INCREMENT PRIMARY KEY,
    service_id INT NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES service_categories(category_id) ON DELETE CASCADE
);

-- Venues table
CREATE TABLE venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    address TEXT NOT NULL,
    city VARCHAR(50) NOT NULL,
    capacity INT,
    price_per_day DECIMAL(10, 2),
    image_path VARCHAR(255),
    rating DECIMAL(3, 1),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Events table
CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    venue_id INT,
    event_name VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    guest_count INT NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    total_amount DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE SET NULL
);

-- Event services mapping
CREATE TABLE event_services (
    event_service_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    service_id INT NOT NULL,
    quantity INT DEFAULT 1,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE
);

-- Testimonials table
CREATE TABLE testimonials (
    testimonial_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE SET NULL
);

-- Blog posts
CREATE TABLE blog_posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    image_path VARCHAR(255),
    author_id INT NOT NULL,
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Gallery items
CREATE TABLE gallery (
    gallery_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    image_path VARCHAR(255) NOT NULL,
    type ENUM('photo', 'video', 'short', 'album') DEFAULT 'photo',
    event_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE SET NULL
);

-- Contact messages
CREATE TABLE contact_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user
INSERT INTO users (username, email, password, first_name, last_name, role)
VALUES ('admin', 'admin@eventmanagement.com', '$2b$12$tGjRpVmcpK9RMjGtMpOw9.XR1eS0Ipjus6F2iXVX.DZj3jdIGdOLK', 'Admin', 'User', 'admin');
-- Password is 'admin123' (hashed)

-- Insert sample service categories
INSERT INTO service_categories (name, description) VALUES 
('Wedding Planners', 'Complete wedding planning services'),
('Destination Wedding', 'Plan your dream wedding at exotic locations'),
('Corporate Event Management', 'Professional corporate event planning'),
('Wedding Photography & Videography', 'Capture your special moments'),
('Catering Service', 'Delicious food for all occasions'),
('Beach Wedding', 'Beautiful ceremonies on the beach'),
('Music & Entertainment', 'Live music and entertainment services'),
('Private Parties', 'Exclusive party planning services');

-- Insert sample services
INSERT INTO services (name, description, price) VALUES
('Full Wedding Planning', 'Complete wedding planning from start to finish', 150000.00),
('Destination Wedding Package', 'All-inclusive destination wedding services', 250000.00),
('Corporate Conference', 'Full conference planning and management', 100000.00),
('Wedding Photography', 'Professional wedding photography services', 50000.00),
('Premium Catering', 'High-end catering for special events', 75000.00),
('Beach Wedding Setup', 'Complete beach wedding arrangement', 120000.00),
('Live Band Performance', 'Live music for your special event', 35000.00),
('Birthday Party Package', 'Complete birthday party planning', 25000.00);

-- Map services to categories
INSERT INTO service_category_mapping (service_id, category_id) VALUES
(1, 1), -- Wedding Planning to Wedding Planners
(2, 2), -- Destination Wedding Package to Destination Wedding
(3, 3), -- Corporate Conference to Corporate Event Management
(4, 4), -- Wedding Photography to Wedding Photography & Videography
(5, 5), -- Premium Catering to Catering Service
(6, 6), -- Beach Wedding Setup to Beach Wedding
(7, 7), -- Live Band Performance to Music & Entertainment
(8, 8); -- Birthday Party Package to Private Parties

-- Insert sample venues
INSERT INTO venues (name, description, address, city, capacity, price_per_day, rating) VALUES
('Pranav Beach Resort', 'Beautiful beach resort for events', 'Chalad, Palliyanmoola', 'Kannur', 200, 75000.00, 4.6),
('Palm Grove Riverside Retreat', 'Serene riverside venue', 'Nattakom', 'Kottayam', 150, 60000.00, 3.9),
('Narayaneeyam Hall', 'Traditional event hall', 'Guruvayoor', 'Thrissur', 300, 50000.00, 4.6),
('Mango County Resort', 'Luxurious resort for events', 'Pirayiri', 'Palakkad', 250, 80000.00, 4.1),
('Namas International Convention Centre', 'Large convention center', 'Guruvayur - Althara', 'Thrissur', 500, 100000.00, 3.9),
('Darsana Villas', 'Private villas for intimate events', 'Kuzhalmannam', 'Palakkad', 100, 45000.00, 4.6),
('Gokulam Park', 'Premium event venue', 'Guruvayur', 'Thrissur', 350, 85000.00, 4.7),
('Rhythm Kumarakom', 'Lakeside event venue', 'Kumarakom', 'Kottayam', 200, 70000.00, 4.5);

-- Insert sample blog posts
INSERT INTO blog_posts (title, content, author_id, is_published, published_at) VALUES
('Legal Requirements for a Destination Wedding in Kerala', 'Kerala, with its tranquil backwaters, verdant landscapes, and enticing beaches, is one of India\'s most popular destination wedding locations...', 1, TRUE, CURRENT_TIMESTAMP),
('Beyond the Backwaters: Unconventional Venues for a Destination Wedding in Kerala', 'When organizing a destination wedding in Kerala, the first things that spring to mind are the beautiful backwaters and beaches...', 1, TRUE, CURRENT_TIMESTAMP),
('The Art of Invitation Card Design: Making a Lasting Impression', 'Invitation cards are one of the most important aspects of any event; they create the first impression and set the tone...', 1, TRUE, CURRENT_TIMESTAMP); 