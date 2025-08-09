from flask import Flask, render_template
from temperature import getSensorData

app = Flask(__name__)

@app.route('/')
def weather():
    temperature1, humidity1, temperature2, humidity2 = getSensorData()
    return render_template('index.html',
                           temperature1=temperature1,
                           humidity1=humidity1,
                           temperature2=temperature2,
                           humidity2=humidity2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
