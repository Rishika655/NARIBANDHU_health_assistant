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
from datetime import datetime, timedelta

@app.route('/cycle', methods=['GET', 'POST'])
def cycle():
    if request.method == 'POST':

        d1 = datetime.strptime(request.form['date1'], "%Y-%m-%d")
        d2 = datetime.strptime(request.form['date2'], "%Y-%m-%d")
        d3 = datetime.strptime(request.form['date3'], "%Y-%m-%d")

        # Calculate cycle lengths
        cycle1 = (d2 - d1).days
        cycle2 = (d3 - d2).days

        avg_cycle = (cycle1 + cycle2) // 2

        # Predict next period
        next_date = d3 + timedelta(days=avg_cycle)

        # Ovulation (approx)
        ovulation = next_date - timedelta(days=14)

        return render_template(
            'cycle_result.html',
            next_date=next_date.date(),
            avg_cycle=avg_cycle,
            ovulation=ovulation.date()
        )

    return render_template('cycle.html')
    

## chatbot route
import random

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    lang = request.args.get('lang', 'en')

    translations = {
        "en": {
            "title": "💬 Health Chatbot",
            "placeholder": "Type your message..."
        },
        "hi": {
            "title": "💬 स्वास्थ्य चैटबॉट",
            "placeholder": "अपना संदेश लिखें..."
        },
        "bn": {
            "title": "💬 স্বাস্থ্য চ্যাটবট",
            "placeholder": "আপনার বার্তা লিখুন..."
        }
    }

    text = translations[lang]

    user_msg = ""
    bot_msg = ""

    if request.method == 'POST':
        user_msg = request.form['message'].lower()

        score = 0
        detected = []

        keywords = {
            "pcos": ["irregular", "missed", "pcos"],
            "hair": ["hairfall", "hair fall"],
            "acne": ["acne", "pimples"],
            "weight": ["weight", "gain"],
            "diet": ["diet", "food", "eat", "nutrition"],
            "period": ["late", "delay", "period"]
        }

        for category, words in keywords.items():
            for word in words:
                if word in user_msg:
                    detected.append(category)
                    score += 1
                    break

        detected = list(set(detected))
        response_parts = []

        if lang == "en":
            if "pcos" in detected:
                response_parts.append("Irregular periods may be linked to hormonal imbalance or PCOS.")

            if "hair" in detected:
                response_parts.append("Hair fall can be due to stress, hormones, or lack of nutrients.")

            if "acne" in detected:
                response_parts.append("Acne is often related to hormonal changes.")

            if "diet" in detected:
                response_parts.append("A balanced diet with iron, protein, and vitamins is important.")

            if "period" in detected:
                response_parts.append("Delayed periods can occur due to stress or hormonal imbalance.")

        elif lang == "hi":
            if "pcos" in detected:
                response_parts.append("अनियमित पीरियड्स हार्मोनल असंतुलन या PCOS का संकेत हो सकते हैं।")

            if "hair" in detected:
                response_parts.append("बाल झड़ना तनाव, हार्मोनल बदलाव या पोषण की कमी के कारण हो सकता है।")

            if "acne" in detected:
                response_parts.append("मुंहासे अक्सर हार्मोनल बदलाव से जुड़े होते हैं।")

            if "diet" in detected:
                response_parts.append("स्वस्थ आहार में आयरन, प्रोटीन और विटामिन शामिल होना चाहिए।")

            if "period" in detected:
                response_parts.append("पीरियड्स में देरी तनाव या हार्मोनल असंतुलन के कारण हो सकती है।")

        elif lang == "bn":
            if "pcos" in detected:
                response_parts.append("অনিয়মিত পিরিয়ড হরমোনের সমস্যা বা PCOS-এর লক্ষণ হতে পারে।")

            if "hair" in detected:
                response_parts.append("চুল পড়া স্ট্রেস, হরমোন বা পুষ্টির অভাবে হতে পারে।")

            if "acne" in detected:
                response_parts.append("ব্রণ সাধারণত হরমোনাল পরিবর্তনের সাথে সম্পর্কিত।")

            if "diet" in detected:
                response_parts.append("সুস্থ খাদ্যাভ্যাসে আয়রন, প্রোটিন ও ভিটামিন থাকা জরুরি।")

            if "period" in detected:
                response_parts.append("পিরিয়ড দেরি হওয়া স্ট্রেস বা হরমোনের কারণে হতে পারে।")

        if lang == "en":
            if score >= 3:
                extra = "Multiple symptoms detected. It is advisable to consult a doctor."
            elif score >= 1:
                extra = "Monitor your health and maintain a healthy lifestyle."
            else:
                extra = "I'm here to help! Try asking about periods, diet, or symptoms."
                

        elif lang == "hi":
            if score >= 3:
                extra = "कई लक्षण पाए गए हैं। डॉक्टर से सलाह लेना उचित होगा।"
            elif score >= 1:
                extra = "अपने स्वास्थ्य पर ध्यान दें और स्वस्थ जीवनशैली बनाए रखें।"
            else:
                extra = "मैं मदद के लिए यहाँ हूँ! पीरियड्स, डाइट या लक्षणों के बारे में पूछें।"

        elif lang == "bn":
            if score >= 3:
                extra = "একাধিক লক্ষণ পাওয়া গেছে। ডাক্তারের পরামর্শ নেওয়া উচিত।"
            elif score >= 1:
                extra = "স্বাস্থ্য ভালো রাখতে জীবনযাত্রার দিকে নজর দিন।"
            else:
                extra = "আমি সাহায্য করার জন্য এখানে আছি! পিরিয়ড বা স্বাস্থ্য নিয়ে প্রশ্ন করুন।"

        if lang == "en":
            heading = "<b>Here's what I found:</b><br><br>"
            note = "<br><br><i>(N.B.: This is general guidance, not medical advice.)</i>"
        elif lang == "hi":
            heading = "<b>यह परिणाम है:</b><br><br>"
            note = "<br><br><i>(नोट: यह सामान्य जानकारी है, चिकित्सा सलाह नहीं है।)</i>"
        elif lang == "bn":
            heading = "<b>এখানে আপনার ফলাফল:</b><br><br>"
            note = "<br><br><i>(দ্রষ্টব্য: এটি সাধারণ তথ্য, চিকিৎসার বিকল্প নয়।)</i>"

        bot_msg = heading + "<br>".join(response_parts)
        bot_msg += "<br><br>" + extra + note


    return render_template(
        'chatbot.html',
        text=text,   
        user_msg=user_msg,
        bot_msg=bot_msg
    )
if __name__ == '__main__':
    app.run(debug=True)