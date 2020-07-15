"use strict"
/**
 * File responsbile for js behavior when it comes to users
 */
import { post_request, get_root_url } from './utils.js'

$(document).ready(async ()=>{
    const logout_button = document.getElementById('logout-button');
    logout_button.addEventListener('click', handle_logout)

})


/**
 * @brief Function to handle the logout of a user
 */
function handle_logout(){
    // Inform backend that the user is being logged out
    const logout_url = "/logout";
    post_request(logout_url, {});

    // Redirect to landing page
    const url_root = get_root_url();
    const landing_path_url = url_root + "/about";
    window.location.href = landing_path_url;
}