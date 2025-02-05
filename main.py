import network
import socket
import time
import dht
import machine

# Wi-Fi credentials
SSID = 'My AP'
PASSWORD = 'MY WIFI PASSWORD'

# Set up DHT11 sensor on GPIO pin 15
sensor = dht.DHT11(machine.Pin(1))

# Set up onboard LED
led = machine.Pin("LED", machine.Pin.OUT)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    # Wait for connection
    while not wlan.isconnected():
        led.value(1)  # Turn on LED
        time.sleep(0.1)
        led.value(0)  # Turn off LED
        time.sleep(0.1)
    
    print('Connected to WiFi')
    print('IP:', wlan.ifconfig()[0])
    led.value(0)  # Ensure LED is off when connected
    return wlan

# Start the web server
def start_server():
    # Create a socket on port 8080
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Listening on", addr)
    
    # Serve requests
    while True:
        cl, addr = s.accept()
        print("Client connected from", addr)
        
        # Blink LED slowly during data transfer
        led.value(1)
        request = cl.recv(1024)
        led.value(0)
        
        request = str(request) 
        
        # Parse GET requests for sensor data
        if '/data' in request:
            # Read sensor
            sensor.measure()
            temperature = str(sensor.temperature()).replace("Â","")
            print(temperature)
            humidity = sensor.humidity()
            
            # Send JSON response
            response = f'{{"temperature": {temperature}, "humidity": {humidity}}}'
            cl.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
            cl.send(response)
        
        # Serve HTML for the main page
        else:
            html = """<!DOCTYPE html>
<html>

<head>
    <title>Current Weather | Tinni</title>
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=DynaPuff:wght@400..700&display=swap" rel="stylesheet">
    <style>
        body {
            /* font-family: Arial, sans-serif; */
            font-family: "Permanent Marker", serif;
            text-align: center;
            /* height: 100vh; */
            padding: 10px;
            background-color: #7b0f33;
            color: white;
        }

        .site_bg {
            background-color: #ffffff31;
            border-radius: 20px;
            padding: 10px;
            margin: 10px;
        }
        .footer_text{
            font-size: 30px;
        }

        .values {
            font-size: 40px;
        }

        .pageHeading {
            font-size: 50px;
        }

        .indicator {
            height: 30px;
            width: 30px;
            background-color: rgba(255, 255, 255, 0.26);
            border-radius: 50%;
            margin: 0px 20px;
        }

        .meter-container {
            width: 80%;
            margin: 20px auto;
        }

        .meter-label {
            margin: 10px 0;
            font-weight: bold;
            font-size: 50px;
        }

        .meter {
            width: 100%;
            height: 40px;
            background-color: #f0f0f043;
            border-radius: 30px;
            overflow: hidden;
            position: relative;
        }

        .temp-meter-fill,
        .hum-meter-fill {
            height: 100%;
            width: 0;
            border-radius: 30px;
            transition: width 0.5s ease;
        }

        .temp-meter-fill {
            background-color: #4CAF50;
        }

        .hum-meter-fill {
            background-color: #2196F3;
        }

        /* font-family: "DynaPuff", system-ui; */
    </style>
    <script>
        async function fetchData() {
            const response = await fetch('/data');
            const data = await response.json();
            console.log(data.temperature);

            document.getElementById("temp").textContent = `${data.temperature} `;
            document.getElementById("deg").style.display = "block";
            document.getElementById("hum").textContent = data.humidity + '%';

            // Update meter fills
            document.getElementById("tempMeterFill").style.width = (data.temperature) + '%';
            document.getElementById("humMeterFill").style.width = data.humidity + '%';
        }
        setInterval(fetchData, 2000); // Fetch data every 2 seconds
    </script>
</head>

<body>
    <div class="site_bg">

        <div style="display: flex; justify-content: center; align-items: center;">
            <p class="indicator" id="indicator"></p>
            <h1 class="pageHeading">Live Weather Station</h1>
        </div>


        <div class="meter-container">
            <div class="meter-label">Temperature</div>
            <div class="meter">
                <div class="temp-meter-fill " id="tempMeterFill"></div>
            </div>
            <div class="" style="display: flex; justify-content: center; align-items: center;">
                <p id="temp" class="values">Loading...</p>
                <p id="deg" style="display: none;" class="values">&deg;C</p>
            </div>

        </div>

        <div class="meter-container">
            <div class="meter-label">Humidity</div>
            <div class="meter">
                <div class="hum-meter-fill" id="humMeterFill"></div>
            </div>
            <p id="hum" class="values">Loading...</p>
        </div>
    </div>

    <div class="site_bg"> 
        <div class="footerBar">
            <p class="footer_text">Rakesh &COPY; 2025 </p>

        </div>
    </div>

            <script>
                setInterval(() => {
                    const blinkDiv = document.getElementById("indicator");
                    blinkDiv.style.backgroundColor =
                        blinkDiv.style.backgroundColor === "red" ? "rgba(255, 255, 255, 0.26)" : "red";
                }, 500); // Change color every 500 milliseconds
            </script>
</body>

</html>"""
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(html)
        
        # Close connection
        cl.close()

# Main program
wlan = connect_wifi()
start_server()

