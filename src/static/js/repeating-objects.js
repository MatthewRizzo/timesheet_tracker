/**
 * File used to instantiate and export objects of classes that would be identical.
 * Creates one point of truth
 */

import {DropdownManagement} from './dropdowns.js'

// Dropdown objects
export const task_dropdown_object = new DropdownManagement('select-task-dropdown', 'placeholder-task-selection');
export const display_dropdown_object = new DropdownManagement('display-task-dropdown', 'placeholder-task-display');