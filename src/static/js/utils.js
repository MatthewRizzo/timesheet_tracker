/**
 * Utility functions that can be used across other files
 */


/**
 * @brief Utility function to maintain alphabetical order of dropdown options
 * @param {ElementId} dropdown_element_id The dropdown being modified
 */
export function maintain_alphabetical_order(dropdown_element_id){
    const jquery_id = "#" + dropdown_element_id;
    const jquery_dropdown = $(jquery_id);
    const dropdown = document.getElementById(dropdown_element_id);

    // Get the sorted option order (from z->a)
    const option_order = $(jquery_id+" option").sort(function (cur_opt, next_opt) {
        return cur_opt.text == next_opt.text ? 0 : cur_opt.text < next_opt.text ? -1 : 1
    });

    // Recreate the options in order (add from z->a) so words alphabetically first will be on top
    jquery_dropdown.empty();
    for(let option of option_order){
        console.log("adding " + option.value)
        dropdown.appendChild(option);
    }

    dropdown.selectedIndex = 0;
}