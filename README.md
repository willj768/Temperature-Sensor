# Temperature Sensor Dashboard

A Flask-based web application that monitors and visualizes temperature and humidity data from two DHT22 sensors using a Raspberry Pi.

## Overview

This project reads sensor data from two DHT22 temperature/humidity sensors, logs the data to a CSV file, and displays real-time readings along with 7-day historical graphs through a web dashboard.

**Features:**
- Real-time temperature and humidity readings from two independent sensors
- Historical data logging to CSV
- Interactive web dashboard with live sensor data
- 7-day temperature and humidity trend graphs
- Automatic data collection and graph updates
- Power management for the outside sensor

## Hardware Requirements

- Raspberry Pi (tested on Pi with GPIO support)
- 2x DHT22 Temperature/Humidity Sensors
- GPIO pins configured as follows:
  - **Sensor 1 (Inside)**: GPIO 17
  - **Sensor 2 (Outside)**: GPIO 27
  - **Power Control**: GPIO 18 (for outside sensor power management)
- Appropriate resistors and wiring for DHT22 sensors

## Software Requirements

- Python 3.7+
- Dependencies (see Installation)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/willj768/Temperature-Sensor.git
   cd Temperature-Sensor
