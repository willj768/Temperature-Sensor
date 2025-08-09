import adafruit_dht
import board
import time

dhtDevice1 = adafruit_dht.DHT22(board.D17)
dhtDevice2 = adafruit_dht.DHT22(board.D27)

def getSensorData():

    try:
        temperature1 = dhtDevice1.temperature
        humidity1 = dhtDevice1.humidity

        temperature2 = dhtDevice2.temperature
        humidity2 = dhtDevice2.humidity
    except RuntimeError as error:
        temperature1 = "Error"
        humidity1 = "Error"

        temperature2 = "Error"
        humidity2 = "Error"

    time.sleep(2)

    return temperature1, humidity1, temperature2, humidity2