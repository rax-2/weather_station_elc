# Pico Weather Station Web App

## Overview
This project is a **Live Weather Station** using a **Raspberry Pi Pico W** and a **DHT11** sensor. It hosts a web interface to display real-time temperature and humidity data fetched from the sensor.

## Features
- Displays **live temperature and humidity** data
- Simple **web UI** built with **HTML, CSS, and JavaScript**
- Data is updated automatically every **2 seconds**
- Uses built-in **MicroPython web server** on Pico W

## Hardware Requirements
- **Raspberry Pi Pico W**
- **DHT11 Sensor** (for temperature & humidity readings)
- **Breadboard & Jumper Wires**

## Software Requirements
- **MicroPython** installed on Pico W
- **Thonny IDE** (for programming & uploading the script)

## Circuit Diagram
![Circuit Diagram](https://github.com/rax-2/weather_station_elc/blob/main/circuit%20diagram.svg)

## Installation & Setup

1. **Flash MicroPython** on your Pico W (if not already installed).
2. **Connect the DHT11** to Pico W as follows:
   - **VCC** → **3.3V**
   - **GND** → **GND**
   - **Data** → **GPIO 1**
3. **Connect Pico W to Wi-Fi** by modifying the SSID and PASSWORD in the script.
4. **Upload the script** (provided in `main.py`) to the Pico W using **Thonny IDE**.
5. **Run the script** and note the IP address assigned to the Pico W.
6. **Access the Web UI** via `http://<your_pico_ip>/` in your browser.

## Usage
- The webpage automatically fetches and updates weather data every 2 seconds.
- Temperature and Humidity are visually represented using meter bars.
- A small red **indicator blinks** to show active data updates.

## API Endpoint
- **`/data`** → Returns sensor readings in JSON format:
```json
{
  "temperature": 21,
  "humidity": 75
}
```

## License
This project is open-source under the **MIT License**.

