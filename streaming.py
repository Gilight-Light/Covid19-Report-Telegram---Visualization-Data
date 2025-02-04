from flask import Flask, jsonify
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/stream', methods=['GET'])
def stream_data():
    data = {
        "province_state": None,
        "country_region": "Country_" + str(random.randint(1, 100)),
        "lat": round(random.uniform(-90, 90), 6),
        "long": round(random.uniform(-180, 180), 6),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "confirmed": random.randint(0, 10000),
        "deaths": random.randint(0, 5000),
        "recovered": random.randint(0, 8000),
        "active": random.randint(0, 1000),
        "who_region": "Region_" + str(random.randint(1, 10))
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
