"use strict"
/**
 * File responsbile for ensure the state of the page is identical each refresh. 
 * Does this through a series of function calls whenever the template is rendered
 */
import { post_request, async_post_request, maintain_alphabetical_order } from './utils.js';
import { add_task } from './task-selection.js';

$(document).ready(async () =>{
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
        await add_task(task, true);
    }

    maintain_alphabetical_order(dropdown_id);
}