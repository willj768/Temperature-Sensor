import datetime
import pandas as pd

def plotGraph():
    data = []
    graphData = []
    now = datetime.datetime.now()

    for i in range (1, 14):
        timeStamp = now - datetime.timedelta(hours=i)
        timeStamp = timeStamp.replace(second=0, microsecond=0)
        data.append(timeStamp)

    df = pd.read_csv("logs.csv")
    df["Time Stamp"] = pd.to_datetime(df["Time Stamp"], errors="coerce")

    for targetTime in data:
        idx = (df["Time Stamp"] - targetTime).abs().idxmin()
        closestRow = df.loc[idx]
        print(f"Target: {targetTime}, Closest CSV time: {closestRow['Time Stamp']}")
        graphData.append(closestRow)

    #print(graphData)
    print(now)
    print("CSV time range:", df["Time Stamp"].min(), "to", df["Time Stamp"].max())
    print(graphData)

plotGraph()
