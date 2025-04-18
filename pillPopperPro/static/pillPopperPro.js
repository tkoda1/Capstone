"use strict"

let socket = null;

function connect_to_server() {
    // let wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:"
    // let url = `${wsProtocol}//${window.location.host}/pillPopperPro/data/`;
    let url = `wss://${window.location.host}/pillPopperPro/data/`;
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


    try {
        const dispense_response = await fetch("/dispense/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ slot: pillSlot })
        })

        if (!dispense_response.ok){
            if (response.status === 400) {
                alert("No more pills to dispense");
                throw new Error("No pills remaining");
            }
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const dispense_data = await dispense_response.json();

        if (!dispense_data.success) {
            alert(dispense_data.error || "Error dispensing pill.");
            throw new Error(`Error: ${dispense_data.error} | Error dispensing pill`)
        }

        const slot_angle = dispense_data.slot_angle
        let ws_message = { action: "release", slot: pillSlot, angle: slot_angle };
        socket.send(JSON.stringify(ws_message));

        if (dispense_data.refill_warning) {
            alert("Warning: Only 3 pills remaining! Refill your machine soon.");
        }

       const update_response = await fetch("/update_taken_times/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ slot: pillSlot, time: timestamp })
        })

        const update_data = await update_response.json();
        console.log("Updated taken times:", update_data.taken_times)
    } catch (error) {
        console.log("Caught error, ", error)
    }

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
    }

    xhr.open("GET", "/pillPopperPro/get-pills", true)
    xhr.send()
}

function pill_refills() {
    console.log('here');
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
    }

    xhr.open("GET", "/pillPopperPro/get-pills", true)
    xhr.send()
}


async function take_and_refill_notification() {
    console.log("Take and refill notification pillpopperpro.js");

    try {
        const refill_reminder = await fetch("/get-refill-reminder/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
        })

        const refill_data = await refill_reminder.json();
        const refills = refill_data.refills;
        const upcoming_refills = refill_data.upcoming_refills;

        const schedule_reminder = await fetch("/get-schedule-reminder/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
        })

        const schedule_data = await schedule_reminder.json();
        const pills = schedule_data.pills;

        const pill_popup = document.getElementById("pillbox-popup-overlay");

        if ((pills.length <= 0) && (refills.length <= 0) && (upcoming_refills.length <= 0)) {
            pill_popup.style.display = "none";
            return;
        }

        pill_popup.style.display = "flex";
        const pill_list = document.getElementById("pill-list");
        const pill_text = document.getElementById("pill-text");
        const refill_list = document.getElementById("refill-list");
        const refill_text = document.getElementById("refill-text");
        const upcoming_refill_list = document.getElementById("upcoming-refill-list");
        const upcoming_refill_text = document.getElementById("upcoming-refill-text");

        if (pills.length > 0) {
            console.log("Pills detected");
            pill_text.style.display = "block";
            pill_list.style.display = "block";
            pill_list.innerHTML = ""; // Clear previous content

            pills.forEach(item => {
                const pillItem = document.createElement("li");
                pillItem.textContent = item;
                pill_list.appendChild(pillItem);
            })
        } else {
            pill_text.style.display = "none";
            pill_list.style.display = "none";
        }

        if (refills.length > 0) {
            console.log("Refills detected");
            refill_text.style.display = "block";
            refill_list.style.display = "block";
            refill_list.innerHTML = ""; // Clear previous content

            refills.forEach(item => {
                const refillItem = document.createElement("li");
                refillItem.textContent = item;
                refill_list.appendChild(refillItem);
            })
        } else {
            refill_text.style.display = "none";
            refill_list.style.display = "none";
        }

        if (upcoming_refills.length > 0) {
            console.log("Upcoming refills detected");
            upcoming_refill_text.style.display = "block";
            upcoming_refill_list.style.display = "block";
            upcoming_refill_list.innerHTML = ""; // Clear previous content

            upcoming_refills.forEach(item => {
                const upcomingRefillItem = document.createElement("li");
                upcomingRefillItem.textContent = item;
                upcoming_refill_list.appendChild(upcomingRefillItem);
            })
        } else {
            upcoming_refill_text.style.display = "none";
            upcoming_refill_list.style.display = "none";
        }

    } catch (error) {
        console.log("Caught error, ", error)
    }
}