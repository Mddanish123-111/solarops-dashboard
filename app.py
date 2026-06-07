from flask import Flask, jsonify, render_template_string, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import random

app = Flask(__name__)

REQUEST_COUNT = Counter('solarops_requests_total', 'Total requests')
PANEL_VOLTAGE = Gauge('solarops_voltage', 'Solar panel voltage')
PANEL_POWER = Gauge('solarops_power_kw', 'Solar panel power output')
PANEL_TEMP = Gauge('solarops_temperature', 'Solar panel temperature')

def generate_solar_data():
    voltage = round(random.uniform(30, 45), 2)
    power = round(random.uniform(1.5, 5.0), 2)
    temp = round(random.uniform(25, 65), 2)
    PANEL_VOLTAGE.set(voltage)
    PANEL_POWER.set(power)
    PANEL_TEMP.set(temp)
    return {
        "panel_id": "PANEL-01",
        "voltage_v": voltage,
        "current_a": round(random.uniform(5, 10), 2),
        "power_kw": power,
        "temperature_c": temp,
        "status": random.choice(["ACTIVE","ACTIVE","ACTIVE","FAULT"])
    }

@app.route('/')
def home():
    REQUEST_COUNT.inc()
    data = generate_solar_data()
    html = """
    <html>
    <head>
        <title>SolarOps Dashboard</title>
        <style>
            body { background:#0a0a0a; color:#00ff88;
                   font-family:Arial; text-align:center; padding:50px; }
            h1 { font-size:40px; }
            .card { background:#1a1a1a; border:1px solid #00ff88;
                    border-radius:10px; padding:20px;
                    margin:20px auto; width:400px; font-size:20px; }
            .fault { color:#ff4444; }
            .active { color:#00ff88; }
        </style>
        <meta http-equiv="refresh" content="3">
    </head>
    <body>
        <h1>☀️ SolarOps Dashboard</h1>
        <div class="card">
            <p>Panel ID: <b>{{ data.panel_id }}</b></p>
            <p>Voltage: <b>{{ data.voltage_v }} V</b></p>
            <p>Current: <b>{{ data.current_a }} A</b></p>
            <p>Power Output: <b>{{ data.power_kw }} kW</b></p>
            <p>Temperature: <b>{{ data.temperature_c }} °C</b></p>
            <p>Status:
                <b class="{{ 'fault' if data.status=='FAULT' else 'active' }}">
                    {{ data.status }}
                </b>
            </p>
        </div>
        <p><a href="/metrics" style="color:#555">View Metrics</a></p>
    </body>
    </html>
    """
    return render_template_string(html, data=data)

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from flask import Response

@app.route('/metrics')
def metrics():
    generate_solar_data()
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/api/data')
def api_data():
    return jsonify(generate_solar_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)