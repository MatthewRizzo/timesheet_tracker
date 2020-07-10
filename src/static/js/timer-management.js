/**
 * File responsbile for js behavior in the Timer panel of the webpage
 */
import {post_request} from './utils.js'

$(document).ready(()=>{
    const start_btn = document.getElementById('start-timer');
    const stop_btn =  document.getElementById('stop-timer');
    start_btn.addEventListener('click', start_timer);
    stop_btn.addEventListener('click', stop_timer);

    // TODO - add set interval and function for updating time once timer started

});


function start_timer(){
    const task = get_current_task();
    toggle_timer_buttons();

    const url = '/start_timer';
    const data = {'task': task};
    post_request(url, data);
}

function stop_timer(){
    const task = get_current_task();
    toggle_timer_buttons();

    const data = {'task': task};
    const url = '/stop_timer';
    post_request(url, data);

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