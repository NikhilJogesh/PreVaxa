from flask import Flask, render_template,request

app = Flask(__name__, static_folder='static')

import random
from datetime import datetime, timedelta

def fetch_random_vaccine_reminders():
    vaccines = [
        "Influenza", "Pneumococcal", "Hepatitis B",
        "Tetanus Booster", "MMR", "Shingles",
        "HPV", "COVID-19 Booster"
    ]
    reminders = []
    for _ in range(3):
        vaccine = random.choice(vaccines)
        age_group = random.choice([
            "0-5 years", "6-12 years", "13-18 years",
            "19-29 years", "30-45 years", "46-59 years", "60+ years"
        ])
        days_ahead = random.randint(5, 60)
        due_date = datetime.now() + timedelta(days=days_ahead)
        due_date_str = due_date.strftime("%d %b %Y")
        reminders.append(
            f"People aged {age_group} should take the {vaccine} vaccine before {due_date_str}."
        )
    return reminders






# Fetch vaccination data from a government API
def fetch_updates_data():
    url = "https://api.covid19india.org/data.json"  # Example API
    response = requests.get(url)
    return response.json()

# Sample static data to simulate update messages
def fetch_updates_data():
    return [
        {"date": "2025-08-01", "message": "New vaccines approved by WHO"},
        {"date": "2025-07-20", "message": "Booster doses recommended for elderly"},
        {"date": "2025-07-10", "message": "Mobile vaccination camps resumed in rural districts"}
    ]

@app.route('/')
def home():
    vaccination_data = fetch_updates_data()
    return render_template('home.html', data=vaccination_data)

@app.route('/updates')
def updates():
    try:
        updates_data = fetch_updates_data()
        random_reminders = fetch_random_vaccine_reminders()  # must call each request
        return render_template(
            'updates.html',
            updates_data=updates_data,
            api_error=None,
            reminders=random_reminders
        )
    except Exception as e:
        return render_template(
            'updates.html',
            updates_data=None,
            api_error=str(e),
            reminders=[]
        )



@app.route('/charts')
def charts():
    return render_template('charts.html')

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    print(fetch_updates_data())  # <-- This will print the update data
    app.run(debug=True)
