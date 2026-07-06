/**
 * TESRECO Intern Portal - Client Side JavaScript Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Navbar Toggle
    const navToggle = document.getElementById('nav-toggle-btn');
    const navMenu = document.getElementById('nav-menu-list');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close menu on navigation link click
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }

    // 2. Active Class Navigation Highlighter
    const currentPath = window.location.pathname;
    const navHome = document.getElementById('nav-home');
    const navAbout = document.getElementById('nav-about');
    const navView = document.getElementById('nav-view');
    const navAdd = document.getElementById('nav-add');
    const navAttendance = document.getElementById('nav-attendance');
    const navMentor = document.getElementById('nav-mentor');
    const navDemo = document.getElementById('nav-demo');

    if (currentPath === '/') navHome?.classList.add('active');
    else if (currentPath === '/about') navAbout?.classList.add('active');
    else if (currentPath === '/view-interns') navView?.classList.add('active');
    else if (currentPath.startsWith('/add-intern')) navAdd?.classList.add('active');
    else if (currentPath === '/attendance') navAttendance?.classList.add('active');
    else if (currentPath === '/assign-mentor') navMentor?.classList.add('active');
    else if (currentPath === '/demo') navDemo?.classList.add('active');

    // 3. Auto-dismiss Flash Messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transform = 'translateX(120%)';
            msg.style.opacity = '0';
            msg.style.transition = 'all 0.5s ease';
            setTimeout(() => {
                msg.remove();
            }, 500);
        }, 5000);
    });

    // 4. Client Side Forms Validation
    const registerForm = document.getElementById('intern-register-form');
    const editForm = document.getElementById('intern-edit-form');

    const validateForm = (form) => {
        if (!form) return true;
        let isValid = true;
        
        const nameField = form.querySelector('#name');
        const emailField = form.querySelector('#email');
        const durationField = form.querySelector('#duration');

        // Reset error messages
        form.querySelectorAll('.error-msg').forEach(el => el.innerText = '');

        if (nameField && nameField.value.trim() === '') {
            const errSpan = form.querySelector('#name-error');
            if (errSpan) errSpan.innerText = 'Name cannot be empty';
            isValid = false;
        }

        if (emailField) {
            const emailVal = emailField.value.trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailVal)) {
                const errSpan = form.querySelector('#email-error');
                if (errSpan) errSpan.innerText = 'Please enter a valid email address';
                isValid = false;
            }
        }

        if (durationField) {
            const durVal = parseInt(durationField.value);
            if (isNaN(durVal) || durVal < 1 || durVal > 12) {
                const errSpan = form.querySelector('#duration-error');
                if (errSpan) errSpan.innerText = 'Duration must be between 1 and 12 months';
                isValid = false;
            }
        }

        return isValid;
    };

    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            if (!validateForm(registerForm)) {
                e.preventDefault();
            }
        });
    }

    if (editForm) {
        editForm.addEventListener('submit', (e) => {
            if (!validateForm(editForm)) {
                e.preventDefault();
            }
        });
    }
});
