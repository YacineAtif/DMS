
    // Construct the WebSocket URL based on the current location
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
    const wsHost = window.location.host; // Host includes hostname and port if applicable
    const wsPath = "/ws/traffic/";
    const trafficSocket = new WebSocket(`${wsScheme}://${wsHost}${wsPath}`);

    trafficSocket.onopen = function(e) {
        console.log("Connection established");
    };

    trafficSocket.onerror = function(error) {
        console.error("WebSocket Error: ", error);
    };


    // Add data row to the traffic data table
    function addTrafficDataRow(data) {
        const tableBody = document.getElementById("trafficDataTable").getElementsByTagName("tbody")[0];
        const newRow = tableBody.insertRow(); // Insert a row at the end of the table

        // Define the order of data for traffic data
        const trafficDataKeys = ['id', 'timestamp', 'x', 'y', 'speed', 'type'];

        trafficDataKeys.forEach(key => {
            const cell = newRow.insertCell();
            cell.textContent = (key === 'x' || key === 'y' || key === 'speed') ? Number(data[key]).toFixed(6) : data[key];
            if (key === 'timestamp') {
                cell.className = 'timestamp-cell'; // Style the timestamp cell if needed
            }
             if (key === 'type') {
                cell.className = 'type-cell'; // Style the type cell
            }
            if (key === 'speed') {
                cell.className = 'speed-cell'; // Apply the class for the speed cell
            }
        });



         // Auto-scroll to the bottom of the table
        const container = document.querySelector(".data-display-container");
        container.scrollTop = container.scrollHeight;
    }


    // Add data row to the driver state data table
    function addDriverStateDataRow(data) {
        const tableBody = document.getElementById("driverStateDataTable").getElementsByTagName("tbody")[0];
        const newRow = tableBody.insertRow(); // Insert a row at the end of the table

        // Define the order of data for driver state
        const driverStateKeys = ['timestamp', 'distraction', 'drowsiness'];

        driverStateKeys.forEach(key => {
            const cell = newRow.insertCell();
            cell.textContent = data[key];
             if (key === 'timestamp') {
                cell.className = 'timestamp-cell'; // Style the timestamp cell
            }

            if (key === 'distraction') {
                cell.className = 'distraction-cell';
            }
            if (key === 'drowsiness') {
                cell.className = 'drowsiness-cell';
            }

        });

        // Auto-scroll to the bottom of the table
        const container = document.querySelector(".table-container");
        container.scrollTop = container.scrollHeight;
    }

    // WebSocket message handling
    trafficSocket.onmessage = function(e) {
        const messageData = JSON.parse(e.data);

        const trafficData = messageData.traffic;
        const driverData = messageData.driver;

        // Add rows to the tables using the data
    if (messageData.hasOwnProperty('traffic')) { // Check if trafficData exists before trying to add it
        addTrafficDataRow(messageData.traffic);
    }

    if (messageData.hasOwnProperty('driver')) { // Check if driverData exists before trying to add it
        addDriverStateDataRow(messageData.driver);
    }

        // Auto-scroll both tables if needed
        document.getElementById("trafficDataTable").parentNode.scrollTop = document.getElementById("trafficDataTable").parentNode.scrollHeight;
        document.getElementById("driverStateDataTable").parentNode.scrollTop = document.getElementById("driverStateDataTable").parentNode.scrollHeight;
    };

    trafficSocket.onclose = function(e) {
        console.error('Webpage closed: Traffic socket closed unexpectedly');
    };

    function clearAndResetSimulation() {

        const traffictableBody = document.getElementById("trafficDataTable").getElementsByTagName("tbody")[0];
        traffictableBody.innerHTML = ''; // Clear the traffic data table body


        const drivertableBody = document.getElementById("driverStateDataTable").getElementsByTagName("tbody")[0];
        drivertableBody.innerHTML = ''; // Clear the driver state dat

        // Send a reset command to the server via WebSocket
        if (trafficSocket.readyState === WebSocket.OPEN) {
            trafficSocket.send(JSON.stringify({ action: 'reset' }));
        } else {
            console.error('WebSocket is not open.');
        }
    }

    function clearData() {
        const traffictableBody = document.getElementById("trafficDataTable").getElementsByTagName("tbody")[0];
        traffictableBody.innerHTML = ''; // Clear the traffic data table body


        const drivertableBody = document.getElementById("driverStateDataTable").getElementsByTagName("tbody")[0];
        drivertableBody.innerHTML = ''; // Clear the driver state dat

    }

    // Optionally, clear data periodically
    setInterval(clearAndResetSimulation, 60000); // Clear data every 60 seconds

    document.getElementById('startBtn').addEventListener('click', function() {
        clearData();
        trafficSocket.send(JSON.stringify({ action: 'start' }));
    });

    document.getElementById('pauseBtn').addEventListener('click', function() {
        trafficSocket.send(JSON.stringify({ action: 'pause' }));
    });

    document.getElementById('resumeBtn').addEventListener('click', function() {
        trafficSocket.send(JSON.stringify({ action: 'resume' }));
    });

    document.getElementById('stopBtn').addEventListener('click', function() {
        if (trafficSocket.readyState === WebSocket.OPEN) {
            clearData();
            trafficSocket.send(JSON.stringify({ action: 'stop' }));
        } else {
            console.error('WebSocket is not open.');
        }
    });
