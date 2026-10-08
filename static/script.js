document.addEventListener('DOMContentLoaded', function () {
    // 1. Client-side validation: Prevent empty to-do titles
    const todoForm = document.querySelector('form[action*="add"]');
    if (todoForm) {
        todoForm.addEventListener('submit', function (e) {
            const titleInput = document.querySelector('input[name="title"]');
            if (titleInput && titleInput.value.trim() === '') {
                e.preventDefault();
                alert('Task title cannot be empty or just whitespace!');
                titleInput.focus();
            }
        });
    }

    // 2. Client-side validation: Check password match on registration
    const registerForm = document.querySelector('#register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            const password = document.querySelector('input[name="password"]').value;
            const confirmPassword = document.querySelector('input[name="confirmation"]').value;
            
            if (password !== confirmPassword) {
                e.preventDefault();
                alert('Passwords do not match!');
            }
        });
    }

    // 3. Bonus Feature: Dark / Light Mode Toggle Logic
    const themeToggleBtn = document.getElementById('theme-toggle');
    if (themeToggleBtn) {
        // Check if user previously selected dark mode
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark-mode');
            themeToggleBtn.textContent = 'Toggle Light Mode';
        }

        themeToggleBtn.addEventListener('click', function () {
            document.body.classList.toggle('dark-mode');
            let theme = 'light';
            if (document.body.classList.contains('dark-mode')) {
                theme = 'dark';
                themeToggleBtn.textContent = 'Toggle Light Mode';
            } else {
                themeToggleBtn.textContent = 'Toggle Dark Mode';
            }
            localStorage.setItem('theme', theme);
        });
    }
});