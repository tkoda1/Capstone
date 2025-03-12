"use strict"

let socket = null;

function connect_to_server() {
    //let wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:"
    //let url = `${wsProtocol}://${window.location.host}/pillPopperPro/data/`;
    let url = `ws://${window.location.host}/pillPopperPro/data/`;
    socket = new WebSocket(url);

    socket.onerror = function(error) {
        displayError("WebSocket Error: " + error)
    }

    socket.onopen = function(event) {
        console.log('Connected to server');
    }

    socket.onclose = function(event) {
        console.log('Disconnected from server');
    }
  
    socket.onmessage = function(event) {
        let response = JSON.parse(event.data);
        console.log(response);
        // FIX THIS
    }
}

// function dispense_pill(pill)
function dispense_pill() {
    console.log("Called dispense_pill function")
    // remove hardcoded data
    let data = {action: "add", slot: "6", dosage: "1"}
    console.log(data)
    console.log(JSON.stringify(data))
    socket.send(JSON.stringify(data))
}

function displayError(message) {
    console.log(message)
}

function updatePage(f, xhr) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        f(response)
        return
    }

    if (xhr.status === 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError(`Received status = ${xhr.status}`)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

// Alerts user to take their medication at the scheduled time
function pill_schedule() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updatePage(update_pill_schedule, xhr)
    }

    xhr.open("GET", "/pillPopperPro/get-pills", true)
    xhr.send()
}

// Alerts users to refill medication at the scheduled time
function pill_refills() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updatePage(update_pill_refills, xhr)
    }

    xhr.open("GET", "/pillPopperPro/get-pills", true)
    xhr.send()
}

function update_pill_schedule(items) {
    if (items['pills'].length == 0) {
        return
    }
    const date = new Date();
    const curr_hour = date.getHours();
    const curr_minute = date.getMinutes();
    let message = "";
    items['pills'].forEach(item => {
        const scheduled_hour = parseInt(item['disposal_time'].substring(0,2));
        const scheduled_minute = parseInt(item['disposal_time'].substring(3));
        if ((scheduled_hour == curr_hour) && 
                (scheduled_minute <= curr_minute) && 
                (item['taken_today'] == 0)) {
            message = message + "\n" + item['name'];
        }
        else if ((scheduled_hour < curr_hour) && (item['taken_today'] == 0)) {
            message = message + "\n" + item['name'];
        }
    })

    // return if no pills remaining to take
    if (message == "") {
        console.log('No pills to take');
        return;
    }
    console.log('Pills to take');
    // alert users of which pills to take
    message = "Hello! You are scheduled to take the following medications:" + 
            message + '\nPlease press OK to dispense medication.';
    // confirm(message); COMMENTED OUT FOR TESTING PURPOSES

    // navigate to dispesning page from here
}

function update_pill_refills(items) {
    if (items['pills'].length == 0) {
        return
    }
    let need_refills = [];
    let upcoming_refills = [];
    let refill_threshold = 10;
    items['pills'].forEach(item => {
        console.log(item);
        if (item['quantity_remaining'] == 0) {
            need_refills.push(item['name'])
            console.log('here')
        }
        else if (item['quantity_remaining'] < refill_threshold) {
            upcoming_refills.push(item['name'])
            console.log('here')
        }
    })

    let message = ""
    if (need_refills.length > 0) {
        message = "The following medication(s) need to be filled: "
        message = message + need_refills.join(", ") + "\n\n"
    }
    if (upcoming_refills.length > 0) {
        message = message + "The following medication(s) are due for a refill: "
        message = message + upcoming_refills.join(", ")
    }
    if (message.length > 0) {
        alert(message)
    }
}