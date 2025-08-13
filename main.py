import threading
import time
import datetime
import pandas as pd
from flask import Flask, render_template
import adafruit_dht
import board
import matplotlib.pyplot as plt
import io
from flask import send_file
import matplotlib.dates as mdates
from gpiozero import OutputDevice

time.sleep(2)

app = Flask(__name__)

PIN_PWR_OUTSIDE = 18 
powerOutside = OutputDevice(PIN_PWR_OUTSIDE, active_high=True, initial_value=False)

def powerOnOutside():
    powerOutside.on()
    time.sleep(2)

def powerOffOutside():
    powerOutside.off()
    time.sleep(1)

dhtDevice1 = adafruit_dht.DHT22(board.D17)
dhtDevice2 = adafruit_dht.DHT22(board.D27)

dataLock = threading.Lock()

csvFile = "logs.csv"
headers = ["TimeStamp", "Temperature1", "Humidity1", "Temperature2", "Humidity2"]

latestData = {
    "temperature1": None,
    "humidity1": None,
    "temperature2": None,
    "humidity2": None,
    "timeStamp": None,
}

filteredGraphData = None

def getSensorData():
    try:
        temperature1 = dhtDevice1.temperature
        humidity1 = dhtDevice1.humidity
        print("[INSIDE WORKING]")
    except RuntimeError as error:
        print("[INSIDE ERROR]", error)
        temperature1 = "Error"
        humidity1 = "Error"

    powerOnOutside()
    try:
        temperature2 = dhtDevice2.temperature
        humidity2 = dhtDevice2.humidity
        print("[OUTSIDE WORKING]")
    except RuntimeError as error:
        print("[OUTSIDE ERROR]", error)
        powerOffOutside()
        time.sleep(1)
        powerOnOutside()
        try:
            temperature2 = dhtDevice2.temperature
            humidity2 = dhtDevice2.humidity
            print("[OUTSIDE WORKING AFTER RESET]")
        except RuntimeError as error2:
            print("[OUTSIDE STILL ERROR]", error2)
            temperature2 = "Error"
            humidity2 = "Error"

    return temperature1, humidity1, temperature2, humidity2


def collectAndLog():
    while True:
        now = datetime.datetime.now()
        timeStamp = now.strftime("%Y-%m-%d %H:%M:%S")

        temperature1, humidity1, temperature2, humidity2 = getSensorData()

        latestData.update({
            "temperature1": temperature1,
            "humidity1": humidity1,
            "temperature2": temperature2,
            "humidity2": humidity2,
            "timeStamp": timeStamp,
        })

        data = [(timeStamp, temperature1, humidity1, temperature2, humidity2)]
        if all(x != "Error" for x in [temperature1, humidity1, temperature2, humidity2]):
            df = pd.DataFrame(data, columns=headers)
            df.to_csv(csvFile, mode='a', header=not pd.io.common.file_exists(csvFile), index=False)

        df = pd.read_csv(csvFile)
        if len(df) > 10080:
            df = df.tail(10080)
            df.to_csv(csvFile, index=False)

        time.sleep(60)

def plotGraph():
    global filteredGraphData

    while True:

        data = []
        graphData = []
        now = datetime.datetime.now()

        for i in range (1, 30):
            timeStamp = now - datetime.timedelta(hours=i)
            timeStamp = timeStamp.replace(second=0, microsecond=0)
            data.append(timeStamp)

        df = pd.read_csv("logs.csv")
        df["TimeStamp"] = pd.to_datetime(df["TimeStamp"], errors="coerce")

        for targetTime in data:
            idx = (df["TimeStamp"] - targetTime).abs().idxmin()
            closestRow = df.loc[idx]
            graphData.append(closestRow)

        dfTemp = pd.DataFrame(graphData)

        with dataLock:
            filteredGraphData = dfTemp

        time.sleep(60)

@app.route('/plot/sensor1.png')
def plotSensor1():
    global filteredGraphData
    
    with dataLock:
        if filteredGraphData is None or filteredGraphData.empty:
            return "No graph data yet", 404
        df = filteredGraphData.copy()

    df.set_index("TimeStamp", inplace=True)

    with dataLock:
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax1.set_title('Inside: Temperature and Humidity Over the Last 7 Days')
        ax1.set_xlabel('Time')

        ax1.xaxis.set_major_locator(mdates.HourLocator(interval=12))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
        ax1.xaxis.set_minor_locator(mdates.HourLocator(interval=1))

        ax1.set_ylabel('Temperature (°C)', color='tab:red')
        ax1.plot(df.index, df['Temperature1'], color='tab:red', label='Temperature 1')
        ax1.tick_params(axis='y', labelcolor='tab:red')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Humidity (%)', color='tab:blue')
        ax2.plot(df.index, df['Humidity1'], color='tab:blue', label='Humidity 1')
        ax2.tick_params(axis='y', labelcolor='tab:blue')

        fig.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close(fig)
        img.seek(0)

    return send_file(img, mimetype='image/png')


@app.route('/plot/sensor2.png')
def plotSensor2():
    global filteredGraphData
    
    with dataLock:
        if filteredGraphData is None or filteredGraphData.empty:
            return "No graph data yet", 404
        df = filteredGraphData.copy()
        
    df.set_index("TimeStamp", inplace=True)

    with dataLock:
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax1.set_title('Outside: Temperature and Humidity Over the Last 7 Days')
        ax1.set_xlabel('Time')

        ax1.xaxis.set_major_locator(mdates.HourLocator(interval=12))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
        ax1.xaxis.set_minor_locator(mdates.HourLocator(interval=1))

        ax1.set_ylabel('Temperature (°C)', color='tab:red')
        ax1.plot(df.index, df['Temperature2'], color='tab:red', label='Temperature 2')
        ax1.tick_params(axis='y', labelcolor='tab:red')

        ax2 = ax1.twinx()
        ax2.set_ylabel('Humidity (%)', color='tab:blue')
        ax2.plot(df.index, df['Humidity2'], color='tab:blue', label='Humidity 2')
        ax2.tick_params(axis='y', labelcolor='tab:blue')

        fig.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close(fig)
        img.seek(0)
    
    return send_file(img, mimetype='image/png')

@app.route('/')
def weather():
    return render_template('index.html',
                           temperature1=latestData["temperature1"],
                           humidity1=latestData["humidity1"],
                           temperature2=latestData["temperature2"],
                           humidity2=latestData["humidity2"],
                           timeStamp=latestData["timeStamp"])

if __name__ == "__main__":
    loggerThread = threading.Thread(target=collectAndLog, daemon=True)
    loggerThread.start()

    graphThread = threading.Thread(target=plotGraph, daemon=True)
    graphThread.start()

    app.run(host='0.0.0.0', port=5000)
