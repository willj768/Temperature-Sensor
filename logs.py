import datetime
import time
import pandas as pd
from temperature import getSensorData

def collectData():
    data = []

    now = datetime.datetime.now()
    timeStamp = now.strftime("%Y-%m-%d %H:%M:%S")

    temperature1, humidity1, temperature2, humidity2 = getSensorData()
    data.append((timeStamp, temperature1, humidity1, temperature2, humidity2))

    return data
    
def exportData(data):
    HEADERS = ["Time Stamp", "Temperature 1", "Humidity 1", "Temperature 2", "Humidity 2"]

    df = pd.DataFrame(data, columns=HEADERS)
    df.to_csv("logs.csv", index=False)


data = collectData()
exportData(data)
time.sleep(10)
