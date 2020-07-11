/**
 * @brief Function to create a class that abstracts common functions for dropdowns
 * @constructor (dropdown_element_id, placeholder_id)
 * @param {string} dropdown_element_id Id of the dropdown to create this class for
 * @param {string} placeholder_id Id of the placeholder_id in the dropdown
 */
export class DropdownManagement {
    constructor(dropdown_element_id, placeholder_id){
        this._dropdown_element_id = dropdown_element_id;
        this._dropdown = document.getElementById(this._dropdown_element_id);
        
        this._dropdown_jquery_id = "#" + this._dropdown_element_id;
        this._jquery_dropdown = $(this._dropdown_jquery_id);

        this._placeholder_id = placeholder_id;
    }

    // Public Functions

    /**
     * 
     * @param {String} option_content The words to use for the option
     */
    add_to_dropdown(option_content){
        this._remove_placeholder_option();

        const is_duplicate = this._check_for_duplicate(option_content);

        if(is_duplicate == false){
            // Create and append the new option
            const new_option = document.createElement('option');
            new_option.value = option_content;
            new_option.text  = option_content;
            this._dropdown.appendChild(new_option);
        }
    }

    /**
     * @returns {HTMLElement} The selected option. To get the value, just do .value
     */
    get_selected_option(){
        return this._dropdown[this._dropdown.selectedIndex];
    }

    get_options_list(){
       return Array.from(this._dropdown.options);
    }

    /**
     * @returns {Number} The number of options
     */
    get_num_options(){
        const options_list = this.get_options_list();
        return options_list.length;
    }

    /**
     * @brief Utility function to maintain alphabetical order of dropdown options
     */
    maintain_alphabetical_order(){
    
        // Get the sorted option order (from z->a)
        const option_order = $(this._dropdown_jquery_id + " option").sort(function (cur_opt, next_opt) {
            return cur_opt.text == next_opt.text ? 0 : cur_opt.text < next_opt.text ? -1 : 1
        });

        // Recreate the options in order (add from z->a) so words alphabetically first will be on top
        this._jquery_dropdown.empty();
        for(let option of option_order){
            this._dropdown.appendChild(option);
        }

        this._dropdown.selectedIndex = 0;
    } // end of maintain_alphabetical_order

    // Private Functions
    /**
     * 
     * @param {String} new_option_text The text of the option being added
     */
    _check_for_duplicate(new_option_text){
        let is_duplicate = false;
        const dropdown_options_array = this.get_options_list();
        for (let option of dropdown_options_array){
            if(option.value == new_option_text){
                is_duplicate = true;
            }
        }
        return is_duplicate;
    } // end of _check_for_duplicates

    /**
     * @brief Utility function to remove the placeholder included before any options are added 
     */
    _remove_placeholder_option(){
        // When adding the first task, the 0th option will always be the placeholder
        const placeholder_option = document.getElementById(this._placeholder_id);
        if (this._dropdown.options[0] == placeholder_option){
            this._dropdown.remove(0)
        }
    }

}