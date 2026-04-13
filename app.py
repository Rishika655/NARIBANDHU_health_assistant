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


if __name__ == '__main__':
    app.run(debug=True)

