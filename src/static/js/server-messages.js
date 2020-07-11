"use strict"
/**
 * File responsible for responding to socket emissions
 */

/**
 * @brief Creates a listener on the socket that executes the callback when data is sent up the socket for that name
 * @param {String} event The flask message to wait for (must be named the same as the flask socket emit)
 * @param {Function} callback A callback function that takes one argument -- response (JSON)
 */
export function create_socket_listener(event, callback) {
    const socket_url = "http://" + document.domain + ":" + location.port;
    const socket = io.connect(socket_url);
    socket.on(event, callback);
}