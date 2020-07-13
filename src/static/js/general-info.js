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
 */
function update_info(response){
    const text_area = document.getElementById('general-info');
    text_area.value = response.info;
}

update_info()

function display_time_diff_after_stop(response){
    const difference = response.difference;
    const task       = response.task;
    const start_time = response.start_time;
    const stop_time  = response.stop_time;
    const text_area = document.getElementById('general-info');

    let msg = "Task " + task + ":" + "\n----------------------\n";
    msg += "\nStart: " + start_time + "\nStop: "+ stop_time + "\nDifference: " + difference + " hours";
    text_area.value = msg;
}