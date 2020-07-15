"use strict"
/**
 * File responsbile for js behavior when it comes to users
 */
import { post_request } from './utils.js'

$(document).ready(async ()=>{
    const logout_button = document.getElementById('logout-button');
    logout_button.addEventListener('click', handle_logout)

})

function handle_logout(){
    const url = "/logout";
    post_request(url, {})
}