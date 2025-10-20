// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(15, 23, 42, 0.98)';
        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
    } else {
        navbar.style.background = 'rgba(15, 23, 42, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards and sections
document.querySelectorAll('.about-card, .team-card, .step, .result-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(el);
});

// Stats counter animation
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

// Trigger counter animation when stats section is visible
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const counters = entry.target.querySelectorAll('.stat h3');
            counters.forEach(counter => {
                const text = counter.textContent;
                if (text.includes('%')) {
                    const num = parseInt(text);
                    counter.textContent = '0%';
                    animateCounter(counter, num);
                    counter.textContent += '%';
                }
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) {
    statsObserver.observe(heroStats);
}

// Mobile menu toggle (if needed in future)
const createMobileMenu = () => {
    const navbar = document.querySelector('.navbar .container');
    const menuBtn = document.createElement('button');
    menuBtn.className = 'mobile-menu-btn';
    menuBtn.innerHTML = '☰';
    menuBtn.style.display = 'none';
    menuBtn.style.fontSize = '1.5rem';
    menuBtn.style.background = 'none';
    menuBtn.style.border = 'none';
    menuBtn.style.color = 'var(--text-primary)';
    menuBtn.style.cursor = 'pointer';
    
    if (window.innerWidth <= 768) {
        menuBtn.style.display = 'block';
    }
    
    navbar.appendChild(menuBtn);
    
    menuBtn.addEventListener('click', () => {
        const navMenu = document.querySelector('.nav-menu');
        navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
        navMenu.style.flexDirection = 'column';
        navMenu.style.position = 'absolute';
        navMenu.style.top = '100%';
        navMenu.style.left = '0';
        navMenu.style.right = '0';
        navMenu.style.background = 'var(--bg-dark)';
        navMenu.style.padding = '1rem';
    });
};

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        const navMenu = document.querySelector('.nav-menu');
        navMenu.style.display = 'flex';
        navMenu.style.flexDirection = 'row';
        navMenu.style.position = 'static';
    }
});

// Add floating particles effect (optional)
const createParticles = () => {
    const hero = document.querySelector('.hero');
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(99, 102, 241, 0.5);
            border-radius: 50%;
            top: ${Math.random() * 100}%;
            left: ${Math.random() * 100}%;
            animation: float ${5 + Math.random() * 10}s infinite ease-in-out;
        `;
        hero.appendChild(particle);
    }
};

// Add CSS animation for particles
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0%, 100% {
            transform: translateY(0) translateX(0);
            opacity: 0;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) translateX(${Math.random() * 100 - 50}px);
        }
    }
`;
document.head.appendChild(style);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    console.log('🤖 MiraiAI Website Loaded Successfully!');
});

// Track bot button clicks
document.querySelectorAll('a[href*="t.me"]').forEach(link => {
    link.addEventListener('click', () => {
        console.log('🚀 User clicked bot link!');
        // You can add analytics tracking here
    });
});

// Zoom state
let currentZoom = 1;
const minZoom = 0.5;
const maxZoom = 3;
const zoomStep = 0.25;

// Lightbox functionality for result images
function openLightbox(imageSrc, title, analysisHTML) {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxTitle = document.getElementById('lightbox-title');
    const lightboxAnalysis = document.getElementById('lightbox-analysis');
    
    lightboxImg.src = imageSrc;
    lightboxTitle.textContent = title;
    lightboxAnalysis.innerHTML = analysisHTML;
    
    // Reset zoom
    currentZoom = 1;
    updateZoom();
    
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.classList.remove('active');
    document.body.style.overflow = ''; // Restore scrolling
    currentZoom = 1; // Reset zoom on close
}

// Zoom functions
function zoomIn() {
    if (currentZoom < maxZoom) {
        currentZoom += zoomStep;
        updateZoom();
    }
}

function zoomOut() {
    if (currentZoom > minZoom) {
        currentZoom -= zoomStep;
        updateZoom();
    }
}

function resetZoom() {
    currentZoom = 1;
    updateZoom();
}

function updateZoom() {
    const img = document.getElementById('lightbox-img');
    const zoomLevel = document.getElementById('zoom-level');
    
    img.style.transform = `scale(${currentZoom})`;
    zoomLevel.textContent = `${Math.round(currentZoom * 100)}%`;
}

// Mouse wheel zoom
document.getElementById('image-wrapper').addEventListener('wheel', (e) => {
    e.preventDefault();
    
    if (e.deltaY < 0) {
        zoomIn();
    } else {
        zoomOut();
    }
}, { passive: false });

// Pan functionality for zoomed images
let isPanning = false;
let startX, startY, scrollLeft, scrollTop;

const imageWrapper = document.getElementById('image-wrapper');

imageWrapper.addEventListener('mousedown', (e) => {
    if (currentZoom > 1) {
        isPanning = true;
        startX = e.pageX - imageWrapper.offsetLeft;
        startY = e.pageY - imageWrapper.offsetTop;
        scrollLeft = imageWrapper.scrollLeft;
        scrollTop = imageWrapper.scrollTop;
    }
});

imageWrapper.addEventListener('mouseleave', () => {
    isPanning = false;
});

imageWrapper.addEventListener('mouseup', () => {
    isPanning = false;
});

imageWrapper.addEventListener('mousemove', (e) => {
    if (!isPanning) return;
    e.preventDefault();
    
    const x = e.pageX - imageWrapper.offsetLeft;
    const y = e.pageY - imageWrapper.offsetTop;
    const walkX = (x - startX) * 2;
    const walkY = (y - startY) * 2;
    
    imageWrapper.scrollLeft = scrollLeft - walkX;
    imageWrapper.scrollTop = scrollTop - walkY;
});

// Close lightbox on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeLightbox();
    }
});

// Add click handlers to result images
document.querySelectorAll('.result-item img').forEach(img => {
    img.addEventListener('click', function() {
        const resultItem = this.closest('.result-item');
        const title = resultItem.querySelector('h3').textContent;
        const analysis = resultItem.querySelector('.analysis');
        
        if (analysis) {
            openLightbox(this.src, title, analysis.innerHTML);
        }
    });
});
