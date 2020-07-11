"use strict"
/**
 * File responsible for all js interactions with the Time Display Panel
 */
import { DropdownManagement } from './dropdowns.js'
import { DynamicInterval } from './dynamic-intervals.js'
import { display_dropdown_object, task_dropdown_object } from './repeating-objects.js'
import { create_socket_listener } from './server-messages.js'
import { async_post_request } from './utils.js'

const wait_for_task_to_display = new DynamicInterval(wait_for_options, 100);
const update_total_time_interval = new DynamicInterval(display_total_time, 500);


$(document).ready(() => {
    // Keep checking until a task option is added, then disable this and activate display total time
    wait_for_task_to_display.activate_interval();
})

/**
 * @brief controls when display_total_time's interval is activated. Once at least one option exists, wait_for_options is deactivated.
 */
function wait_for_options() {
    if(display_dropdown_object.get_selected_option().value != display_dropdown_object.get_placeholder_element().value){
        console.log("turning on display_total_time")
        // It is now safe to poll for total time.
        update_total_time_interval.activate_interval();
    
        // It is no longer necessary to poll and check if a task is selected
        wait_for_task_to_display.deactivate_interval();
    }
}

/**
 * @brief Function to be called by set interval. Gets the current total time for the selected task and displays it.
 * @Note By default, this function will not be called by interval. It is deactivated until at least one option is present
 */
async function display_total_time (){
    console.log('calling display_total_time')
    const url = '/get_total_time';
    const task = display_dropdown_object.get_selected_option().value;
    const data = {'task': task};
    const response = await async_post_request(url, data)
    const total_time = response.total_time;
    const units =      response.units;

    const display_id = 'total-time';
    const display_element = document.getElementById(display_id);
    display_element.value = total_time + ' ' + units;
}

/**
 * Every time the task selection dropdown is changed, the Time Display Dropdown needs to be modified to match
 * @precondition The Task Selection dropdown has been sorted
 */
export function copy_tasks_to_display_dropdown(){
    // Clear the current display dropdown
    display_dropdown_object.clear_dropdown();

    // The options most be inserted from z->a so that a is on top
    let task_options = task_dropdown_object.get_options_list();
    const src_dropdown = task_dropdown_object.get_dropdown();
    const dst_dropdown = display_dropdown_object.get_dropdown();
    dst_dropdown.innerHTML = src_dropdown.innerHTML;

    display_total_time();
}