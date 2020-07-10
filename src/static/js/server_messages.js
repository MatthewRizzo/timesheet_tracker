/**
 * File responsible for responding to socket emissions
 */

$(document).ready(() =>{
    $( async () => {
    // maybe io.connect
    const url_connecting_to = "http://" + document.domain + ":" + location.port;
    const cur_socket = io.connect(url_connecting_to);
        cur_socket.on('test', (response)  => {
            const msg = response['content'];
        })
    })
})

// meant for case when timer to short 