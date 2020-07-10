"use strict"
/**
 * Utility functions that can be used across other files
 */


/**
 * @brief Utility function to maintain alphabetical order of dropdown options
 * @param {string} dropdown_element_id The dropdown being modified
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
        dropdown.appendChild(option);
    }

    dropdown.selectedIndex = 0;
}

/**
 * 
 * @param {JSON} data_json The Json of data to send to the backend. Will be stringified by this function
 * @param {string} url the url to perform the post request for
 */
export function post_request(url, data_json){
    $.post({
        url: url,
        data: JSON.stringify(data_json),
        dataType: 'application/json',
        
        success: function(){},
        error: function(request, status, error){
            console.log("Failed post request for url " + url);
            console.log("Error " + error);
            console.log("Status " + status);
        }
    });
}

/**
 * @brief Utility function to abstract away repetition of async post requests
 * @param {string} url Url to post request for
 * @param {JSON} data_json Data to send in post request
 */
export async function async_post_request(url, data_json) { 
    let response = '';
    try{
        response = await $.post({
            url: url,
            data: JSON.stringify(data_json),
            dataType: 'json',

        });
    }catch (error){
        console.log("Failed post request for url " + url);
        console.log(JSON.stringify(error));
        response = 'ERROR';
    }

    return response
}