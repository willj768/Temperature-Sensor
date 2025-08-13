import datetime
import time
import pandas as pd
from temperature import getSensorData

def collectAndLog():
    HEADERS = ["Time Stamp", "Temperature 1", "Humidity 1", "Temperature 2", "Humidity 2"]
    CSV_FILE = "logs.csv"

    while True:
        now = datetime.datetime.now()
        timeStamp = now.strftime("%Y-%m-%d %H:%M:%S")

        temperature1, humidity1, temperature2, humidity2 = getSensorData()
        data = [(timeStamp, temperature1, humidity1, temperature2, humidity2)]

        df = pd.DataFrame(data, columns=HEADERS)
        df.to_csv(CSV_FILE, index=False)

        print(f"Logged data at {timeStamp}")

        time.sleep(10) 

if __name__ == "__main__":
    collectAndLog()
