"use strict"
/**
 * File responsbile for ensure the state of the page is identical each refresh. 
 * Does this through a series of function calls whenever the template is rendered
 */
import { post_request, async_post_request } from './utils.js';
import { DropdownManagement } from './dropdowns.js'
import { enable_start_timer } from './task-selection.js'
import { task_dropdown_object } from './repeating-objects.js';
import { copy_tasks_to_display_dropdown, make_time_display_header } from './time-display.js';


$(document).ready(async () =>{
    const time_display_json = make_time_display_header();
    time_display_json.time_box.value = time_display_json.header;
    await startup_load_data();
    await synchronize_task_dropdown();

});

/**
 * @brief Asks backend for a list of currently known tasks and adds them to the dropdowns
 */
async function synchronize_task_dropdown(){
    const url = "/get_task_list";
    const response_dict = await async_post_request(url, {});
    const task_list = response_dict.task_list;
    if(task_list == "ERROR"){
        console.error("No Valid Task List received. Cannot Add to Dropdown")
        return
    }else if(task_list == []){
        return
    }

    const dropdown_id = 'select-task-dropdown';

    for (let task of task_list){
        task_dropdown_object.add_to_dropdown(task);
        copy_tasks_to_display_dropdown();

    }
    task_dropdown_object.maintain_alphabetical_order(dropdown_id);
    enable_start_timer(task_dropdown_object);
}

/**
 * @brief Tells backend to load any data stored from previous runs into its time manager
 */
async function startup_load_data(){
    const url = "load_data_at_startup";
    const load_data_response = await async_post_request(url, {});

    if(load_data_response == 'NACK'){
        alert("There was an issue loading in previous data. Please restart the program / contact a developer")
        return
    }

}