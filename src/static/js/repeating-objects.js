/**
 * File used to instantiate and export objects of classes that would be identical.
 * Creates one point of truth
 */

import {DropdownManagement} from './dropdowns.js'

export const task_dropdown_object = new DropdownManagement('select-task-dropdown', 'placeholder-task');