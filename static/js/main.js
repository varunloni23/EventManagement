// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        var flashMessages = document.querySelectorAll('.alert');
        flashMessages.forEach(function(message) {
            var bsAlert = new bootstrap.Alert(message);
            bsAlert.close();
        });
    }, 5000);
    
    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Service filter functionality
    const serviceFilters = document.querySelectorAll('.service-filter');
    if (serviceFilters.length > 0) {
        serviceFilters.forEach(filter => {
            filter.addEventListener('click', function() {
                const category = this.getAttribute('data-category');
                
                // Remove active class from all filters
                serviceFilters.forEach(f => f.classList.remove('active'));
                
                // Add active class to clicked filter
                this.classList.add('active');
                
                // Show/hide services based on category
                const services = document.querySelectorAll('.service-item');
                services.forEach(service => {
                    if (category === 'all' || service.getAttribute('data-category') === category) {
                        service.style.display = 'block';
                    } else {
                        service.style.display = 'none';
                    }
                });
            });
        });
    }
    
    // Event date validation
    const eventDateInput = document.getElementById('event_date');
    if (eventDateInput) {
        const today = new Date().toISOString().split('T')[0];
        eventDateInput.setAttribute('min', today);
        
        eventDateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const currentDate = new Date();
            
            if (selectedDate < currentDate) {
                this.value = today;
                alert('Please select a future date for your event.');
            }
        });
    }
    
    // Price range slider
    const priceRange = document.getElementById('price-range');
    const priceOutput = document.getElementById('price-output');
    
    if (priceRange && priceOutput) {
        priceOutput.textContent = priceRange.value;
        
        priceRange.addEventListener('input', function() {
            priceOutput.textContent = this.value;
        });
    }
    
    // Image preview for file uploads
    const imageInputs = document.querySelectorAll('.image-upload');
    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const preview = document.getElementById(this.getAttribute('data-preview'));
            if (preview) {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    };
                    reader.readAsDataURL(this.files[0]);
                }
            }
        });
    });
    
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add parallax effect to hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.scrollY;
            if (scrollPosition < 600) {
                const yPos = scrollPosition * 0.3;
                heroSection.style.backgroundPositionY = `-${yPos}px`;
            }
        });
    }
    
    // Image hover zoom effect
    const zoomImages = document.querySelectorAll('.zoom-effect');
    zoomImages.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            this.style.transition = 'transform 0.5s ease';
        });
        
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Counter animation
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
        const counterObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = parseInt(counter.getAttribute('data-target'));
                    const duration = 2000; // 2 seconds
                    const step = target / (duration / 16); // 16ms per frame (approx 60fps)
                    
                    let current = 0;
                    const updateCounter = () => {
                        current += step;
                        counter.innerText = Math.round(current);
                        
                        if (current < target) {
                            requestAnimationFrame(updateCounter);
                        } else {
                            counter.innerText = target;
                        }
                    };
                    
                    updateCounter();
                    observer.unobserve(counter);
                }
            });
        }, { threshold: 0.5 });
        
        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }
    
    // Testimonial carousel autoplay
    const testimonialCarousel = document.getElementById('testimonialCarousel');
    if (testimonialCarousel) {
        new bootstrap.Carousel(testimonialCarousel, {
            interval: 5000
        });
    }
    
    // Gallery lightbox
    const galleryItems = document.querySelectorAll('.gallery-item');
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const imgSrc = this.querySelector('img').getAttribute('src');
            const title = this.querySelector('img').getAttribute('alt');
            
            // Create modal if it doesn't exist
            let modal = document.getElementById('galleryModal');
            if (!modal) {
                modal = document.createElement('div');
                modal.id = 'galleryModal';
                modal.className = 'modal fade';
                modal.innerHTML = `
                    <div class="modal-dialog modal-lg modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header border-0">
                                <h5 class="modal-title"></h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body p-0">
                                <img src="" class="img-fluid" alt="">
                            </div>
                        </div>
                    </div>
                `;
                document.body.appendChild(modal);
            }
            
            // Set modal content
            modal.querySelector('.modal-title').textContent = title;
            modal.querySelector('.modal-body img').setAttribute('src', imgSrc);
            modal.querySelector('.modal-body img').setAttribute('alt', title);
            
            // Show modal
            const modalInstance = new bootstrap.Modal(modal);
            modalInstance.show();
        });
    });
    
    // Add gold accent to first letter of headings
    document.querySelectorAll('h1, h2').forEach(heading => {
        if (heading.textContent.trim().length > 0 && !heading.classList.contains('no-first-letter')) {
            const text = heading.textContent;
            const firstLetter = text.charAt(0);
            const restOfText = text.slice(1);
            
            heading.innerHTML = `<span class="first-letter">${firstLetter}</span>${restOfText}`;
        }
    });
    
    // Add hover effect to service and venue cards
    const cards = document.querySelectorAll('.service-card, .venue-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('card-hover');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('card-hover');
        });
    });
}); 