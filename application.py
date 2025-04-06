from flask import Flask, request, render_template_string, url_for
import os
import joblib
import pandas as pd
import numpy as np

application = Flask(__name__)
application.secret_key = 'super-secret'

DAYLIGHT_GROUPS = {
    "aspen": {'13:52': 0, '13:53': 1, '13:54': 2, '13:55': 3},
    "montgomery": {'13:27': 0, '13:28': 1, '13:29': 2, '13:30': 3},
    "great-smoky-mountain": {'13:38': 0, '13:39': 1, '13:40': 2, '13:41': 3},
    "shenandoah-national-park": {'13:49': 0, '13:50': 1, '13:51': 2, '13:52': 3},
    "berkshire": {'14:04': 0, '14:05': 1, '14:06': 2, '14:07': 3},
    "franconia-notch-state-park": {'14:13': 0, '14:14': 1, '14:15': 2, '14:16': 3},
    "lost-maple-state-park": {'13:19': 0, '13:20': 1, '13:21': 2, '13:22': 3},
    "pere-marquette-state-park": {'13:51': 0, '13:52': 1, '13:53': 2, '13:54': 3},
    "traverse-city": {'14:17': 0, '14:18': 1, '14:19': 2, '14:20': 3},
    "superior-national-forest": {'14:33': 0, '14:34': 1, '14:35': 2, '14:36': 3},
    "spearfish-canyon": {'14:15': 0, '14:16': 1, '14:17': 2, '14:18': 3},
    "zion-national-park": {'13:45': 0, '13:46': 1, '13:47': 2, '13:48': 3},
    "logan-canyon": {'14:03': 0, '14:04': 1, '14:05': 2, '14:06': 3},
    "yellowstone-national-park": {'14:16': 0, '14:17': 1, '14:18': 2, '14:19': 3},
    "eastern-sierra": {'13:41': 0, '13:42': 1, '13:43': 2, '13:44': 3},
    "columbia-river-george": {'14:22': 0, '14:23': 1, '14:24': 2, '14:25': 3},
    "levenworth": {'13:52': 0, '13:53': 1, '13:54': 2, '13:55': 3}
}

FOLIAGE_LABELS = {
    1: "Early September",
    2: "Mid September",
    3: "Late September",
    4: "Early October",
    5: "Mid October",
    6: "Late October",
    7: "Early November",
    8: "Mid November",
    9: "Late November"
}

def load_models():
    models = {}
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    for file in os.listdir(model_dir):
        if file.endswith('.pkl'):
            name = file.replace('.pkl', '')
            models[name] = joblib.load(os.path.join(model_dir, file))
    return models

models = load_models()

def predict(model, precip, temp, daylight_group):
    df = pd.DataFrame([{
        'Precip': precip,
        'Temp': temp,
        'Daylight_Group': daylight_group
    }])
    pred = model.predict(df)
    pred = np.clip(np.round(pred), 1, 9).astype(int)
    pred[0][1] = max(pred[0][0], pred[0][1])
    pred[0][2] = max(pred[0][1], pred[0][2])
    return {
        'Low-Mod': FOLIAGE_LABELS[int(pred[0][0])],
        'Peak': FOLIAGE_LABELS[int(pred[0][1])],
        'Past-Peak': FOLIAGE_LABELS[int(pred[0][2])]
    }

@application.route('/')
def home():
    links = "".join(
        f"<a href='/{loc}'>{loc.replace('-', ' ').title()}</a><br>"
        for loc in DAYLIGHT_GROUPS.keys()
    )
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
        <title>Fall Foliage Predictor</title>
    </head>
    <body>
        <h1>Annual Fall Foliage ML Model</h1>
        {{ links|safe }}
        <br><br>
        <a href="{{ url_for('static', filename='instructions.pdf') }}" target="_blank">
            <button type="button">Documentation</button>
        </a>
    </body>
    </html>
    ''', links=links)

def generate_location_page(location):
    def location_func():
        times = list(DAYLIGHT_GROUPS[location].keys())
        prediction = None
        if request.method == 'POST':
            time = request.form['time']
            temp = float(request.form['temp'])
            precip = float(request.form['precip'])
            daylight_group = DAYLIGHT_GROUPS[location][time]
            model = models[location]
            prediction = predict(model, precip, temp, daylight_group)
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
            <title>{{ location.replace('-', ' ').title() }}</title>
        </head>
        <body>
            <form method="POST">
                <h1>Welcome to {{ location.replace('-', ' ').title() }}!</h1>
                <label>Average Daylight-Time:</label><br>
                <select name="time">
                    <option value="" disabled selected>Select</option>
                    {% for t in times %}
                        <option value="{{ t }}">{{ t }}</option>
                    {% endfor %}
                </select><br><br>
                <label>Average Temperature (°F):</label><br>
                <input type="number" step="0.1" name="temp" placeholder="e.g. 62.5" required><br><br>
                <label>Average Precipitation (inches):</label><br>
                <input type="number" step="0.01" name="precip" placeholder="e.g. 1.23" required><br><br>
                <button type="submit">Submit</button>
                <button type="button" onclick="location.href='/'">Home</button>
                <a href="{{ url_for('static', filename='instructions.pdf') }}" target="_blank">
                    <button type="button">Instructions</button>
                </a>
            </form>
            {% if prediction %}
                <h2>Prediction:</h2>
                <ul>
                    <li>Low-Mod: {{ prediction['Low-Mod'] }}</li>
                    <li>Peak: {{ prediction['Peak'] }}</li>
                    <li>Past-Peak: {{ prediction['Past-Peak'] }}</li>
                </ul>
            {% endif %}
        </body>
        </html>
        ''', location=location, times=times, prediction=prediction)
    application.add_url_rule(f"/{location}", endpoint=f"{location}_page", view_func=location_func, methods=["GET", "POST"])

for loc in DAYLIGHT_GROUPS:
    generate_location_page(loc)

if __name__ == "__main__":
    application.run(debug=True)
