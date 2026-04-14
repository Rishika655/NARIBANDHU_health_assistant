## import Flask
from flask import Flask, render_template, request
from datetime import datetime, timedelta

## create app object
app = Flask(__name__)

## Home route
@app.route('/')
def home():
    return render_template('index.html')

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
if __name__ == '__main__':
    app.run(debug=True)