/**
 * File Responsible for handling all events on the landing page
 */
$(document).ready(() =>{
    const register_button = document.getElementById('landing-page-register-button');
    const login_button = document.getElementById('landing-page-login-button');
    const register_page_url = "http://localhost:5000/register";
    const login_page_url    = "http://localhost:5000/login";

    register_button.addEventListener('click', () => {
        window.location.href = register_page_url;
    });
    login_button.addEventListener('click', () => {
        window.location.href = login_page_url;
    });

});

