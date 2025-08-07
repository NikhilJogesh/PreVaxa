from flask import Flask, render_template,request

app = Flask(__name__)

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
        return render_template('updates.html', updates_data=updates_data, api_error=None)
    except Exception as e:
        return render_template('updates.html', updates_data=None, api_error=str(e))

@app.route('/charts')
def charts():
    return render_template('charts.html')

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    print(fetch_updates_data())  # <-- This will print the update data
    app.run(debug=True)
