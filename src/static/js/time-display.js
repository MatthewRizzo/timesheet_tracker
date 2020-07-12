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
const update_total_time_interval = new DynamicInterval(display_times, 500);


$(document).ready(() => {
    // Keep checking until a task option is added, then disable this and activate display total time
    wait_for_task_to_display.activate_interval();
})

/**
 * @brief Wrapper function to update the total time and time list box's
 */
function display_times(){
    display_total_time();
    display_time_list();
}

/**
 * @returns {{
 *      time_box: HTMLElement, 
 *      header: string,
 * }} 
 * The header of the time display and its container html element. 
 *     The time box element to put the time sets in.
 *     The string header to put in the display box
 */
export function make_time_display_header(){
    const return_json = {};
    return_json.header = "Start\t\tStop\t\tDifference\n--------------------------------------------\n";
    return_json.time_box  = document.getElementById('time-display-box');
    return return_json;
}

/**
 * @brief controls when display_time's interval is activated. Once at least one option exists, wait_for_options is deactivated.
 */
function wait_for_options() {
    if(display_dropdown_object.get_selected_option().value != display_dropdown_object.get_placeholder_element().value){
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
 * @brief Gets all completed time segments for the currently selected task and dispalys them
 */
async function display_time_list(){
    // Get the time list and units from backend
    const url = '/get_completed_times';
    const task = display_dropdown_object.get_selected_option().value;
    const data = {'task': task};
    const response = await async_post_request(url, data);
    const time_list = response.time_list;
    const units =     response.units;

    // Display the results where appropriate
    const display_json = make_time_display_header();
    let display_msg = display_json.header;
    if(time_list != null){
        for(let time_set of time_list){
            const start_time = time_set[0];
            const end_time   = time_set[1];
            const diff_time  = time_set[2];
            display_msg += start_time + "\t" + end_time + '\t' + diff_time;
            display_msg += '\n';
        }
    }
    display_json.time_box.value = display_msg;
}

/**
 * Every time the task selection dropdown is changed, the Time Display Dropdown needs to be modified to match
 * @precondition The Task Selection dropdown has been sorted
 */
export function copy_tasks_to_display_dropdown(){
    const selected_value_before = display_dropdown_object.get_selected_option().value;
    // Clear the current display dropdown
    display_dropdown_object.clear_dropdown();

    // The options most be inserted from z->a so that a is on top
    let task_options = task_dropdown_object.get_options_list();
    const src_dropdown = task_dropdown_object.get_dropdown();
    const dst_dropdown = display_dropdown_object.get_dropdown();
    dst_dropdown.innerHTML = src_dropdown.innerHTML;

    display_dropdown_object.set_selected(selected_value_before);
    display_total_time();
    display_time_list();
}