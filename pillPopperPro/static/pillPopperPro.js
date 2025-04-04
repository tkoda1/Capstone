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

    // CODE THAT USES MQTT
    // document.getElementById("dispense-btn").addEventListener("click", function() {
    //     socket.send(JSON.stringify({ command: "DISPENSE" }));
    // });
    
    // socket.onmessage = function(event) {
    //     const data = JSON.parse(event.data);
    //     alert(data.message);  
    // };
}

// function dispense_pill(pill)
async function dispense_pill() {
    console.log("Called dispense_pill function");
    const pillImageElement = document.getElementById("id_pill_picture");
    const pillSlot = pillImageElement.getAttribute("data-slot");

    console.log("Pill Slot Detected:", pillSlot);

    if (!["1", "2", "3", "4", "5", "6"].includes(pillSlot)) {
        displayError("Invalid pill slot");
        return;
    }

    const timestamp = new Date().toISOString().replace("Z", "+00:00");

    await fetch("/dispense/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ slot: pillSlot })
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 400) {
                alert("No more pills to dispense");
                throw new Error("No pills remaining");
            }
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Server Response:", data);
        if (data.success) {
            // send message to ws to release 
            console.log(data)
            const slot_angle = data.slot_angle
            let ws_message = { action: "release", slot: pillSlot, angle: slot_angle };
            socket.send(JSON.stringify(ws_message));

            console.log(`Updated quantity_remaining: ${data.quantity_remaining}`);
            
            if (data.refill_warning) {
                alert("Warning: Only 3 pills remaining! Refill your machine soon.");
            }
        } else {
            alert(data.error || "Error dispensing pill.");
        }
    })
    .catch(error => console.error("Fetch error:", error));
    
    
    


    await fetch("/update_taken_times/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ slot: pillSlot, time: timestamp })
    })
    .then(response => response.json())
    .then(data => console.log("Updated taken times:", data.taken_times))
    .catch(error => console.error("Error updating taken times:", error));
}


function getCSRFToken() {
        let token = document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken'))
            ?.split('=')[1];

        if (!token) {
            console.error("CSRF Token not found!");
        }
        return token;
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


function pill_schedule() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updatePage(update_pill_schedule, xhr)
    }

    xhr.open("GET", "/pillPopperPro/get-pills", true)
    xhr.send()
}

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
    if (items['pills'].length === 0) {
        return;
    }
    
    const date = new Date();
    const curr_hour = date.getHours();
    const curr_minute = date.getMinutes();
    let message = "";

    items['pills'].forEach(item => {
        item['disposal_times'].forEach(time => {  
            const scheduled_hour = parseInt(time.substring(0, 2));
            const scheduled_minute = parseInt(time.substring(3));

            if ((scheduled_hour === curr_hour && scheduled_minute <= curr_minute && item['taken_today'] === 0) ||
                (scheduled_hour < curr_hour && item['taken_today'] === 0)) {
                message += "\n" + item['name'];
            }
        });
    });

    if (message === "") {
        console.log('No pills to take');
        return;
    }

    console.log('Pills to take');
    
    message = "Hello! You are scheduled to take the following medications:" + 
              message + '\nPlease press OK to dispense medication.';
    // confirm(message); COMMENTED OUT FOR TESTING PURPOSES
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