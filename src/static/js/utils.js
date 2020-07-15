"use strict"
/**
 * Utility functions that can be used across other files
 */

/**
 * 
 * @param {JSON} data_json The Json of data to send to the backend. Will be stringified by this function
 * @param {string} url the url to perform the post request for
 */
export function post_request(url, data_json){
    $.post({
        url: url,
        data: JSON.stringify(data_json),
        contentType: 'application/json',
        
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
    let response = null;
    try{
        response = await $.post({
            url: url,
            data: JSON.stringify(data_json),
            contentType: 'application/json',

        });
    }catch (error){
        console.log("Failed post request for url " + url);
        console.log(JSON.stringify(error));
        response = 'ERROR';
    }

    return response
}


/**
 * @return The root url of the appilcation (i.e. localhost:5000/)
 */
export function get_root_url(){
    const url_root = "http://" + document.domain + ":" + location.port;
    return url_root
}