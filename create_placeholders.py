from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(filename, width, height, text, bg_color=(200, 200, 200), text_color=(80, 80, 80)):
    """Create a placeholder image with specified dimensions and text."""
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font, fallback to default if not available
    try:
        font = ImageFont.truetype("Arial", 30)
    except IOError:
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    try:
        # For newer Pillow versions
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        text_width = right - left
        text_height = bottom - top
    except AttributeError:
        # For older Pillow versions
        text_width, text_height = draw.textsize(text, font=font)
    
    position = ((width - text_width) // 2, (height - text_height) // 2)
    
    # Draw text
    draw.text(position, text, fill=text_color, font=font)
    
    # Save image
    img.save(filename)
    print(f"Created placeholder image: {filename}")

def main():
    # Create images directory if it doesn't exist
    os.makedirs('static/images', exist_ok=True)
    
    # Create placeholder images
    placeholders = [
        ('static/images/logo.png', 200, 60, 'EMK Logo', (30, 43, 58), (212, 175, 55)),
        ('static/images/hero1.jpg', 1200, 600, 'Wedding Event'),
        ('static/images/hero2.jpg', 1200, 600, 'Corporate Event'),
        ('static/images/hero3.jpg', 1200, 600, 'Private Party'),
        ('static/images/service-placeholder.jpg', 400, 300, 'Service Image'),
        ('static/images/venue-placeholder.jpg', 400, 300, 'Venue Image'),
        ('static/images/about.jpg', 600, 400, 'About Us'),
        ('static/images/header-bg.jpg', 1200, 300, 'Header Background'),
        ('static/images/testimonial-bg.jpg', 1200, 600, 'Testimonial Background'),
        ('static/images/cta-bg.jpg', 1200, 400, 'CTA Background'),
        ('static/images/blog-placeholder.jpg', 400, 300, 'Blog Image'),
    ]
    
    for placeholder in placeholders:
        if len(placeholder) == 4:
            create_placeholder_image(*placeholder)
        else:
            create_placeholder_image(*placeholder)

if __name__ == "__main__":
    main() 