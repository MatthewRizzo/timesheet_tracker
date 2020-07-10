/**
 * File responsbile for js behavior in the task selection panel of the webpage
 */

import { maintain_alphabetical_order } from './utils.js'

$(document).ready(()=>{
    const submit_task_btn = document.getElementById("submit-new-task")
    submit_task_btn.addEventListener('click', add_task);
})

/**
 * @brief Reads in input task and adds it to dropdown, ignores if empty
 */
function add_task(){
    const dropdown_id = 'select-task-dropdown';
    const dropdown = document.getElementById(dropdown_id);
    const placeholder_id = 'placeholder-task';
    const new_task_input = document.getElementById("add-new-task");

    // Get task input
    const new_task = new_task_input.value;
    new_task_input.value = '';
    if(new_task == ''){
        return
    }

    remove_placeholder_option(dropdown, placeholder_id);

    // Create and append the new option
    const new_option = document.createElement('option');
    new_option.value = new_task;
    new_option.text  = new_task;
    dropdown.appendChild(new_option);


    maintain_alphabetical_order(dropdown_id);
}


function remove_placeholder_option(dropdown_element, placeholder_id){
    // When adding the first task, the 0th option will always be the placeholder
    const placeholder_option = document.getElementById(placeholder_id);
    console.log(dropdown_element.options[0].value)
    console.log(placeholder_option)
    if (dropdown_element.options[0] == placeholder_option){
        dropdown_element.remove(0)
    }
}