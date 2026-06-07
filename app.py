from flask import Flask, jsonify, render_template_string
import random
import time

app = Flask(__name__)

def generate_solar_data():
    return {
        "panel_id": "PANEL-01",
        "voltage_v": round(random.uniform(30, 45), 2),
        "current_a": round(random.uniform(5, 10), 2),
        "power_kw": round(random.uniform(1.5, 5.0), 2),
        "temperature_c": round(random.uniform(25, 65), 2),
        "status": random.choice([
            "ACTIVE", "ACTIVE", "ACTIVE", "FAULT"
        ])
    }

@app.route('/')
def home():
    data = generate_solar_data()
    html = """
    <html>
    <head>
        <title>SolarOps Dashboard</title>
        <style>
            body {
                background: #0a0a0a;
                color: #00ff88;
                font-family: Arial;
                text-align: center;
                padding: 50px;
            }
            h1 { font-size: 40px; }
            .card {
                background: #1a1a1a;
                border: 1px solid #00ff88;
                border-radius: 10px;
                padding: 20px;
                margin: 20px auto;
                width: 400px;
                font-size: 20px;
            }
            .fault { color: #ff4444; }
            .active { color: #00ff88; }
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
                <b class="{{ 'fault' if data.status == 'FAULT'
                             else 'active' }}">
                    {{ data.status }}
                </b>
            </p>
        </div>
        <p style="color:#555">Auto-refreshes every 3 seconds</p>
    </body>
    </html>
    """
    return render_template_string(html, data=data)

@app.route('/api/data')
def api_data():
    return jsonify(generate_solar_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)