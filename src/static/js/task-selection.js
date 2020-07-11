"use strict"
/**
 * File responsbile for js behavior in the task selection panel of the webpage
 */

import { async_post_request, post_request } from './utils.js';
import { DropdownManagement } from './dropdowns.js'
import { task_dropdown_object } from './repeating-objects.js'
import { copy_tasks_to_display_dropdown } from './time-display.js'

$(document).ready(() => {
    const submit_task_btn = document.getElementById("submit-new-task");
    submit_task_btn.addEventListener('click', read_new_task);
})

/**
 * @brief Reads in input task and adds it to dropdown, ignores if empty
 */
async function read_new_task(){
    const dropdown_id = 'select-task-dropdown';
    const new_task_input = document.getElementById("add-new-task");
    
    // Get task input
    const new_task = new_task_input.value;
    new_task_input.value = '';
    if(new_task == ''){
        return
    }

    task_dropdown_object.add_to_dropdown(new_task);
    task_dropdown_object.maintain_alphabetical_order();
    copy_tasks_to_display_dropdown();
    await backend_add_task(new_task);
}

/** 
 * @brief Enable the start button once the first valid task has been added
 * @param {DropdownManagement} dropdown_class_object An object representing the dropdown
 */
export function enable_start_timer(dropdown_class_object){
    if(dropdown_class_object.get_num_options() > 0){
        const start_button = document.getElementById('start-timer');
        start_button.disabled = false;
    }
}
/**
 * @brief Wrapper for adding a new task to the tracked task list on the backend
 * @param {string} task_name The name of the task to add
 * @return {Boolean} true if the task is a duplicate, false otherwise
 */
async function backend_add_task(task_name) {
    const url = '/add_task';
    const data = {'new_task' : task_name};
    const response = await async_post_request(url, data);
    if(response == "Already Added"){
        return true;
    }else
    return false;
}