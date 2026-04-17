## import Flask
from flask import Flask, render_template, request
from datetime import datetime, timedelta

## create app object
app = Flask(__name__)

## Home route
@app.route('/')
def home():
    return render_template('index.html')

## Menu
@app.route('/menu')
def menu():
    return render_template('menu.html')

## Predict route
@app.route('/predict', methods=['POST'])
def predict():
    last_period = request.form['last_period']
    last_date = datetime.strptime(last_period, "%Y-%m-%d")

    next_date = last_date + timedelta(days=28)

    return render_template('result.html', result=next_date.date()) ##connect python to html

## Get the PCOS form
@app.route('/pcos', methods=['GET'])
def pcos_page():
    return render_template('pcos.html')

## Predict score
@app.route('/pcos', methods=['POST'])
def pcos():
    irregular = int(request.form['irregular'])
    weight = int(request.form['weight'])
    acne = int(request.form['acne'])
    hair = int(request.form['hair'])
    hairfall = int(request.form['hairfall'])

    score = irregular + weight + acne + hair + hairfall

    if score >= 4:
        risk = " 🔴High Risk 🔴"
        color = "red"
        message = "⚠️ You may be showing several symptoms associated with PCOS. It is recommended to consult a healthcare professional."
        tips = [
            "👩‍⚕️ Consult a doctor for proper diagnosis",
            "🥗 Maintain a balanced diet",
            "🏃‍♀️ Exercise regularly",
            "🧘 Reduce stress through yoga or meditation"
        ]

    elif score >= 2:
        risk = "🟠 Moderate Risk 🟠"
        color = "orange"
        message = "⚠️ You show some signs related to PCOS. Monitoring your health and lifestyle is advised."
        tips = [
            "📅 Track your menstrual cycle regularly",
            "🍔 Avoid junk food and excess sugar",
            "🚶‍♀️ Stay physically active",
            "😴 Maintain a healthy sleep schedule"
        ]

    else:
        risk = "🟢 Low Risk 🟢"
        color = "green"
        message = "✅ You currently show minimal symptoms related to PCOS. Keep maintaining a healthy lifestyle."
        tips = [
            "🥦 Continue healthy eating habits",
            "🏃 Stay active daily",
            "📝 Keep monitoring your cycle",
            "💧 Stay hydrated and stress-free"
        ]

    return render_template(
        'pcos_result.html',
        result=risk,
        color=color,
        message=message,
        tips=tips
    )



## cycle tracker
@app.route('/tracker', methods=['GET'])
def tracker_page():
    return render_template('tracker.html')

@app.route('/tracker', methods=['POST'])
def tracker():
    last_period = request.form['last_period']
    cycle_length = int(request.form['cycle'])

    last_date = datetime.strptime(last_period, "%Y-%m-%d")

    next_period = last_date + timedelta(days=cycle_length)
    ovulation = next_period - timedelta(days=14)
    fertile_start = ovulation - timedelta(days=2)
    fertile_end = ovulation + timedelta(days=2)

    return render_template(
        'tracker_result.html',
        next_period=next_period.date(),
        ovulation=ovulation.date(),
        fertile_start=fertile_start.date(),
        fertile_end=fertile_end.date()
    )


## add route for symptom checker
@app.route('/symptom', methods=['GET'])
def symptom_page():
    return render_template('symptom.html')

## processing
@app.route('/symptom', methods=['POST'])
def symptom():
    text = request.form['symptoms'].lower()

    score = 0

    if "irregular" in text:
        score += 1
    if "weight" in text:
        score += 1
    if "acne" in text:
        score += 1
    if "hair" in text:
        score += 1

    if score >= 3:
        risk = "High Risk"
    elif score >= 1:
        risk = "Moderate Risk"
    else:
        risk = "Low Risk"

    return render_template('symptom_result.html', result=risk)
















if __name__ == '__main__':
    app.run(debug=True)