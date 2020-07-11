"use strict"
/**
 * File responsible for all js interactions with the Time Display Panel
 */
import { display_dropdown_object, task_dropdown_object } from './repeating-objects.js'
import { DropdownManagement } from './dropdowns.js'

$(document).ready(() => {

});

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

}