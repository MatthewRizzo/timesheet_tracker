/**
 * File Responsible for handling all events on the landing page
 */

import { get_root_url } from './utils.js'

$(document).ready(() =>{
    const register_button = document.getElementById('landing-page-register-button');
    const login_button = document.getElementById('landing-page-login-button');
    const url_root = get_root_url();
    const register_page_url = url_root + "/register";
    const login_page_url    = url_root + "/login";

    register_button.addEventListener('click', () => {
        window.location.href = register_page_url;
    });
    login_button.addEventListener('click', () => {
        window.location.href = login_page_url;
    });

});

