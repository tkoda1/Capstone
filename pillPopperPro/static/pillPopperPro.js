function displayError(message) {
    console.log(message)
}

function updatePage(xhr) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        update_pill_schedule(response)
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
        updatePage(xhr)
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
        return
    }

    // alert users of which pills to take
    message = "Hello! You are scheduled to take the following medications:" + 
            message + '\nPlease press OK to dispense medication.';
    // confirm(message); COMMENTED OUT FOR TESTING PURPOSES

    // navigate to dispesning page from here
}