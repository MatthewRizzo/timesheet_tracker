"use strict"
/**
 * File responsbile for js behavior in the Timer panel of the webpage
 */
import {async_post_request, post_request} from './utils.js';
import { DynamicInterval } from './dynamic-intervals.js'
import { task_dropdown_object } from './repeating-objects.js'
import { create_socket_listener } from './server-messages.js'

// Update the time display every .1 seconds
const stopwatch_interval = new DynamicInterval(display_current_difference, 100);
$(document).ready(async ()=>{
    const start_btn = document.getElementById('start-timer');
    const stop_btn =  document.getElementById('stop-timer');
    start_btn.addEventListener('click', start_timer);
    stop_btn.addEventListener('click', stop_timer);
    create_socket_listener('logout', handle_logout)
});


function start_timer(){
    const task = get_current_task();
    toggle_timer_buttons();

    const url = '/start_timer';
    const data = {'task': task};
    post_request(url, data);
    stopwatch_interval.activate_interval();
    
}

function stop_timer(){
    const task = get_current_task();
    toggle_timer_buttons();

    const data = {'task': task};
    const url = '/stop_timer';
    post_request(url, data);
    stopwatch_interval.deactivate_interval();

}

async function display_current_difference(){
    const url = '/get_current_diff';
    const cur_task = task_dropdown_object.get_selected_option().value;
    const response = await async_post_request(url, {'task': cur_task});
    const time_diff = response.time_diff;
    const units     = response.units;

    const display_box = document.getElementById('stopwatch');
    display_box.value = time_diff + " " + units;

}

/**
 * @returns {string} The task_name currently selected by the dropdown
 */
function get_current_task(){
    const task_dropdown = document.getElementById('select-task-dropdown');
    const selectedOption = task_dropdown[task_dropdown.selectedIndex];
    return selectedOption.value;
}

/**
 * @brief Utility function to toggle disabled status of the buttons
 */
function toggle_timer_buttons(){
    const start_btn = document.getElementById('start-timer');
    const stop_btn =  document.getElementById('stop-timer');

    // toggle start
    if (start_btn.disabled == true){
        start_btn.disabled = false;
    }
    else{
        start_btn.disabled = true;
    }

    // toggle stop
    if (stop_btn.disabled == true){
        stop_btn.disabled = false;
    }
    else{
        stop_btn.disabled = true;
    }
}

/**
 * @brief Cleans up anything created in this file that needs to be stopped/deleted on logout
 */
function handle_logout(){
    stopwatch_interval.deactivate_interval();
}