import time
import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT22(board.D17)

while True:
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        print(f"Temp: {temperature:.1f} °C  Humidity: {humidity:.1f} %")

    except RuntimeError as error:
        print(f"Reading error: {error}")

    time.sleep(60)
