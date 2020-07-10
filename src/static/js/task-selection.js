"use strict"
/**
 * File responsbile for js behavior in the task selection panel of the webpage
 */

import { maintain_alphabetical_order, async_post_request, post_request } from './utils.js';


$(document).ready(() => {
    const submit_task_btn = document.getElementById("submit-new-task");
    submit_task_btn.addEventListener('click', read_new_task);
})

/**
 * @brief Adds a task to the dropdown and the backend
 * @param {string} new_task The new task to add to the dropdown
 * @param {Boolean} is_initializing When true, new tasks will not be added to the backed (because they already exist there)
 */
export async function add_task(new_task, is_initializing){
    const dropdown_id = 'select-task-dropdown';
    const dropdown = document.getElementById(dropdown_id);
    const placeholder_id = 'placeholder-task';
    remove_placeholder_option(dropdown, placeholder_id);

    if(is_initializing == false){
        await backend_add_task(new_task);
    }

    // Create and append the new option
    const new_option = document.createElement('option');
    new_option.value = new_task;
    new_option.text  = new_task;
    dropdown.appendChild(new_option);


}

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

    add_task(new_task, false);

    maintain_alphabetical_order(dropdown_id);
}

/**
 * @brief Utility function to remove the placeholder included before any options are added 
 * @param {HTMLElement} dropdown_element The element for the dropdown
 * @param {string} placeholder_id The id of the placholder (to try and remove it)
 */
function remove_placeholder_option(dropdown_element, placeholder_id){
    // When adding the first task, the 0th option will always be the placeholder
    const placeholder_option = document.getElementById(placeholder_id);
    if (dropdown_element.options[0] == placeholder_option){
        dropdown_element.remove(0)
    }

    // Enable the start button once the first valid task has been added
    const start_button = document.getElementById('start-timer');
    start_button.disabled = false;
}

/**
 * @brief Wrapper for adding a new task to the tracked task list on the backend
 * @param {string} task_name The name of the task to add
 */
async function backend_add_task(task_name) {
    const url = '/add_task';
    const data = {'new_task' : task_name};
    post_request(url, data);
}