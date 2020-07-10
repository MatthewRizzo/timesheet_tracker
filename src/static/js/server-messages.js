"use strict"
/**
 * File responsible for responding to socket emissions
 */

$(document).ready(() =>{
    const url_connecting_to = "http://" + document.domain + ":" + location.port;
    const socket = io.connect(url_connecting_to);

    socket.on('update_info', (response) => {
        const text_area = document.getElementById('general-info');
        text_area.value = response.info;
    });

    // Below are all the socket emissions being waited on. Can be called using send_to_client() in python
    socket.on('stop_timer_diff', (response) => {
        const difference = response.difference;
        const task       = response.task;
        const start_time = response.start_time;
        const stop_time  = response.stop_time;
        const text_area = document.getElementById('general-info');

        let msg = "Task " + task + ":" + "\n----------------------\n";
        msg += "\nStart: " + start_time + "\nStop: "+ stop_time + "\nDifference: " + difference + "hours";
        text_area.value = msg;

    });
});

// meant for case when timer to short 