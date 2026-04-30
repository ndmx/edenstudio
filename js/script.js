// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerOffset = 80;
            const elementPosition = target.offsetTop;
            const offsetPosition = elementPosition - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Mobile menu toggle (only if elements exist)
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });
}

// Navbar background change on scroll
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Active navigation link highlighting (only if sections exist)
const sections = document.querySelectorAll('section');
const navLinks = document.querySelectorAll('.nav-link');

if (sections.length > 0 && navLinks.length > 0) {
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= sectionTop) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').substring(1) === current) {
                link.classList.add('active');
            }
        });
    });
}

// Improved Intersection Observer for staggered animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('animate-in')) {
            // Add staggered delay for elements within the same container
            const elements = Array.from(entry.target.querySelectorAll('.panel-card, .experience-card, .project-card, .timeline-item, .doc-list-item, .contact-card, .stat-card, .showcase-card'));
            elements.forEach((element, index) => {
                setTimeout(() => {
                    element.classList.add('animate-in');
                }, index * 100); // 100ms stagger between elements
            });

            // Add animation to the main container
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

// Observe all sections and major content blocks for animation
document.querySelectorAll('section, .hero-content, .hero-visual').forEach(element => {
    observer.observe(element);
});

// Improved parallax effect for hero section with throttling (only if hero exists)
let ticking = false;
window.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(() => {
            const scrolled = window.pageYOffset;
            const rate = Math.min(scrolled * -0.3, 0); // Limit the parallax effect
            const heroVisual = document.querySelector('.hero-visual');

            if (heroVisual) {
                heroVisual.style.transform = `translateY(${rate}px)`;
            }
            ticking = false;
        });
        ticking = true;
    }
});

// Add smooth reveal animations for hero elements (only if they exist)
document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('loaded');

    // Add subtle entrance animations to hero elements (only on index page)
    const heroElements = document.querySelectorAll('.hero-title, .hero-subtitle, .hero-buttons, .cycling-card');
    if (heroElements.length > 0) {
        heroElements.forEach((element, index) => {
            setTimeout(() => {
                element.classList.add('animate-in');
            }, 100 + index * 200);
        });
    }

    // Cycling card functionality (only on index page)
    const cyclingCard = document.querySelector('.cycling-card');
    if (cyclingCard) {
        const cardContents = cyclingCard.querySelectorAll('.card-content');
        if (cardContents.length > 0) {
            let currentIndex = 0;
            let cycleInterval;

            function cycleCard() {
                // Remove active class from current
                cardContents[currentIndex].classList.remove('active');

                // Move to next card
                currentIndex = (currentIndex + 1) % cardContents.length;

                // Add active class to new current
                cardContents[currentIndex].classList.add('active');
            }

            function startCycling() {
                cycleInterval = setInterval(cycleCard, 2000);
            }

            function stopCycling() {
                clearInterval(cycleInterval);
            }

            // Start cycling
            startCycling();

            // Pause cycling on hover
            cyclingCard.addEventListener('mouseenter', stopCycling);
            cyclingCard.addEventListener('mouseleave', startCycling);
        }
    }
});

// Back to Top Button Functionality
const backToTopButton = document.getElementById('backToTop');
if (backToTopButton) {
    // Show/hide back to top button based on scroll position
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    });

    // Smooth scroll to top when clicked
    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Table of Contents Smooth Scrolling
document.querySelectorAll('.toc-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            const headerOffset = 100;
            const elementPosition = targetElement.offsetTop;
            const offsetPosition = elementPosition - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Highlight current section in TOC
const tocLinks = document.querySelectorAll('.toc-link');
const docSections = document.querySelectorAll('.doc-section');

if (tocLinks.length > 0 && docSections.length > 0) {
    window.addEventListener('scroll', () => {
        let current = '';
        
        docSections.forEach(section => {
            const sectionTop = section.offsetTop - 150;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= sectionTop) {
                current = section.getAttribute('id');
            }
        });

        tocLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
}

// Enhanced mobile menu for new pages
document.addEventListener('DOMContentLoaded', function() {
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        const navToggle = document.querySelector('.nav-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        if (navToggle && navMenu && navMenu.classList.contains('active')) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        }
    });

    // Handle escape key to close mobile menu
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const navToggle = document.querySelector('.nav-toggle');
            const navMenu = document.querySelector('.nav-menu');
            
            if (navToggle && navMenu && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        }
    });
});
