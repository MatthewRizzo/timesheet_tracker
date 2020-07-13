"use strict"
/**
 * File responsible for functionality of interacting with the General Information Panel
 */

import { create_socket_listener } from './server-messages.js'

$(document).ready(() =>{
    create_socket_listener('update_info', update_info);
    create_socket_listener('stop_timer_diff', display_time_diff_after_stop);

})

/**
 * 
 * @param  {JSON} response Has the key info  which is message printed
 * @brief Updates the General Information box with the 
 * @note Should be the ONLY function by which the General Information tab's text is modified 
 */
function update_info(response){
    const seperator = "\n---------------------------------------\n\n";
    const text_area = document.getElementById('general-info');
    const prev_text = text_area.value;

    const new_text = prev_text + response.info + seperator;

    // Clear the text area and set it to the new text
    text_area.value = '';
    text_area.value += new_text;
}

function display_time_diff_after_stop(response){
    const difference = response.difference;
    const task       = response.task;
    const start_time = response.start_time;
    const stop_time  = response.stop_time;
    const response_json = {};
    
    let msg = "Task " + task + ":" + "\n";
    msg += "\nStart: " + start_time + "\nStop: "+ stop_time + "\nDifference: " + difference + " hours";
    response_json.info = msg;

    update_info(response_json);
}