from flask import Flask, render_template,request, jsonify
import requests
import random
from datetime import datetime, timedelta
import math
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__, static_folder='static')

# MongoDB Configuration
# Replace with your MongoDB connection string
# MONGO_URI = "mongodb://localhost:27017/"  # For local development
MONGO_URI = "mongodb+srv://nikhiljogesh2007:WTlDG4oVFLSwJOzo@maincluster.4phxhnd.mongodb.net/?retryWrites=true&w=majority&appName=MainCluster"  # For cloud MongoDB Atlas

# Fallback in-memory storage
fallback_records = []

try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,  # 5 second timeout
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
        maxPoolSize=10,
        retryWrites=True
    )
    # Test the connection
    client.admin.command('ping')
    db = client['prevax_db']
    vaccine_records = db['vaccine_records']
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Falling back to local storage simulation...")
    client = None
    db = None
    vaccine_records = fallback_records

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

def fetch_vaccine_centers(lat=None, lon=None):
    """
    Fetch vaccine centers near the given coordinates.
    First tries to get real data from internet, falls back to randomized data.
    """
    try:
        # Try to fetch real data from a healthcare API
        # This is a placeholder - in real implementation, you'd use actual healthcare APIs
        # For now, we'll generate realistic randomized data
        raise Exception("API not available - using fallback data")

    except Exception:
        # Generate randomized vaccine center data
        center_names = [
            "City General Hospital Vaccination Center",
            "Community Health Center - Vaccine Hub",
            "Metro Medical Center Immunization Clinic",
            "Regional Healthcare Vaccination Site",
            "Primary Care Vaccine Distribution Center",
            "Municipal Health Department Vaccine Center",
            "District Hospital Immunization Unit",
            "Neighborhood Health Clinic - Vaccines",
            "Central Medical Complex Vaccine Hub",
            "Public Health Vaccination Facility"
        ]

        centers = []
        base_lat = lat if lat else 40.7128  # Default to NYC coordinates
        base_lon = lon if lon else -74.0060

        for i in range(5):
            # Generate random coordinates within ~10km radius
            lat_offset = random.uniform(-0.05, 0.05)
            lon_offset = random.uniform(-0.05, 0.05)

            center_lat = base_lat + lat_offset
            center_lon = base_lon + lon_offset

            # Calculate distance using Haversine formula
            def calculate_distance(lat1, lon1, lat2, lon2):
                R = 6371  # Earth's radius in kilometers
                dlat = math.radians(lat2 - lat1)
                dlon = math.radians(lon2 - lon1)
                a = (math.sin(dlat/2) * math.sin(dlat/2) +
                     math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
                     math.sin(dlon/2) * math.sin(dlon/2))
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                return R * c

            distance = calculate_distance(base_lat, base_lon, center_lat, center_lon)

            centers.append({
                'name': center_names[i],
                'distance': round(distance, 2),
                'lat': center_lat,
                'lon': center_lon,
                'address': f"Street {random.randint(100, 999)}, District {random.randint(1, 20)}",
                'phone': f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                'hours': "Mon-Fri: 9:00 AM - 5:00 PM, Sat: 9:00 AM - 2:00 PM"
            })

        # Sort by distance
        centers.sort(key=lambda x: x['distance'])
        return centers

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

def calculate_age_from_dob(dob_str):
    """Calculate age from date of birth string (YYYY-MM-DD format)"""
    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except:
        return None

def get_recommended_vaccines(age):
    """Get recommended vaccines based on age"""
    vaccines = []

    if age < 1:
        vaccines = [
            {"name": "Hepatitis B", "doses": 3, "schedule": "Birth, 1-2 months, 6-18 months"},
            {"name": "DTaP (Diphtheria, Tetanus, Pertussis)", "doses": 5, "schedule": "2, 4, 6, 15-18 months, 4-6 years"},
            {"name": "Hib (Haemophilus influenzae type b)", "doses": 4, "schedule": "2, 4, 6, 12-15 months"},
            {"name": "Polio (IPV)", "doses": 4, "schedule": "2, 4, 6-18 months, 4-6 years"},
            {"name": "PCV13 (Pneumococcal)", "doses": 4, "schedule": "2, 4, 6, 12-15 months"}
        ]
    elif 1 <= age < 2:
        vaccines = [
            {"name": "MMR (Measles, Mumps, Rubella)", "doses": 2, "schedule": "12-15 months, 4-6 years"},
            {"name": "Varicella (Chickenpox)", "doses": 2, "schedule": "12-15 months, 4-6 years"},
            {"name": "Hepatitis A", "doses": 2, "schedule": "12-23 months, 6 months later"}
        ]
    elif 2 <= age < 11:
        vaccines = [
            {"name": "Annual Influenza", "doses": 1, "schedule": "Yearly"},
            {"name": "DTaP Booster", "doses": 1, "schedule": "4-6 years (if not completed)"}
        ]
    elif 11 <= age < 18:
        vaccines = [
            {"name": "Tdap (Tetanus, Diphtheria, Pertussis)", "doses": 1, "schedule": "11-12 years"},
            {"name": "HPV (Human Papillomavirus)", "doses": 2, "schedule": "11-12 years, 6 months apart"},
            {"name": "Meningococcal ACWY", "doses": 2, "schedule": "11-12 years, 16 years"},
            {"name": "Annual Influenza", "doses": 1, "schedule": "Yearly"}
        ]
    elif 18 <= age < 65:
        vaccines = [
            {"name": "Annual Influenza", "doses": 1, "schedule": "Yearly"},
            {"name": "Td/Tdap", "doses": 1, "schedule": "Every 10 years"},
            {"name": "COVID-19", "doses": 2, "schedule": "Primary series + boosters as recommended"},
            {"name": "HPV", "doses": 3, "schedule": "Up to age 26 (if not previously vaccinated)"}
        ]
    else:  # 65+
        vaccines = [
            {"name": "Annual Influenza", "doses": 1, "schedule": "Yearly"},
            {"name": "Pneumococcal (PPSV23)", "doses": 1, "schedule": "65+ years"},
            {"name": "Shingles (Zoster)", "doses": 2, "schedule": "60+ years, 2-6 months apart"},
            {"name": "Td/Tdap", "doses": 1, "schedule": "Every 10 years"},
            {"name": "COVID-19", "doses": 2, "schedule": "Primary series + boosters as recommended"}
        ]

    return vaccines

def generate_vaccine_id():
    """Generate a random 7-digit vaccine ID"""
    return random.randint(1000000, 9999999)

def search_vaccine_record(vaccine_id, dob):
    """Search for vaccine record in MongoDB"""
    if vaccine_records is None:
        return None

    if isinstance(vaccine_records, list):
        for record in vaccine_records:
            if record['vaccine_id'] == int(vaccine_id) and record['date_of_birth'] == dob:
                return record
        return None

    try:
        record = vaccine_records.find_one({
            "vaccine_id": int(vaccine_id),
            "date_of_birth": dob
        })
        return record
    except Exception as e:
        print(f"Database search error: {e}")
        return None

def register_vaccine_record(dob):
    """Register new vaccine record in MongoDB"""
    if vaccine_records is None:
        return None

    if isinstance(vaccine_records, list):
        vaccine_id = generate_vaccine_id()
        while any(record['vaccine_id'] == vaccine_id for record in vaccine_records):
            vaccine_id = generate_vaccine_id()

        record = {
            "vaccine_id": vaccine_id,
            "date_of_birth": dob,
            "registration_date": datetime.now().isoformat(),
            "vaccines_taken": [],
            "next_due": []
        }
        vaccine_records.append(record)
        return vaccine_id

    try:
        # Generate unique vaccine ID
        vaccine_id = generate_vaccine_id()
        while vaccine_records.find_one({"vaccine_id": vaccine_id}):
            vaccine_id = generate_vaccine_id()

        # Create new record
        record = {
            "vaccine_id": vaccine_id,
            "date_of_birth": dob,
            "registration_date": datetime.now().isoformat(),
            "vaccines_taken": [],
            "next_due": []
        }

        result = vaccine_records.insert_one(record)
        if result.inserted_id:
            return vaccine_id
        return None
    except Exception as e:
        print(f"Database registration error: {e}")
        return None

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

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/vaxiradar')
def vaxiradar():
    return render_template('vaxiradar.html')

@app.route('/vaxisearch')
def vaxisearch():
    return render_template('vaxisearch.html')

@app.route('/api/vaccine-centers')
def api_vaccine_centers():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    centers = fetch_vaccine_centers(lat, lon)
    return jsonify(centers)

@app.route('/api/search-vaccine-record', methods=['POST'])
def api_search_vaccine_record():
    data = request.get_json()
    vaccine_id = data.get('vaccine_id')
    dob = data.get('date_of_birth')

    if not vaccine_id or not dob:
        return jsonify({"error": "Missing vaccine ID or date of birth"}), 400

    # Search in database
    record = search_vaccine_record(vaccine_id, dob)

    if record:
        # Calculate age and get recommendations
        age = calculate_age_from_dob(dob)
        if age is not None:
            recommended_vaccines = get_recommended_vaccines(age)
            return jsonify({
                "found": True,
                "vaccine_id": record['vaccine_id'],
                "age": age,
                "recommended_vaccines": recommended_vaccines,
                "registration_date": record.get('registration_date', 'Unknown')
            })

    return jsonify({"found": False, "error": "Vaccine record not found"})

@app.route('/api/register-vaccine-record', methods=['POST'])
def api_register_vaccine_record():
    data = request.get_json()
    dob = data.get('date_of_birth')

    if not dob:
        return jsonify({"error": "Missing date of birth"}), 400

    # Register new record
    vaccine_id = register_vaccine_record(dob)

    if vaccine_id:
        # Calculate age and get recommendations
        age = calculate_age_from_dob(dob)
        if age is not None:
            recommended_vaccines = get_recommended_vaccines(age)
            return jsonify({
                "success": True,
                "vaccine_id": vaccine_id,
                "age": age,
                "recommended_vaccines": recommended_vaccines
            })

    return jsonify({"success": False, "error": "Registration failed"}), 500

if __name__ == '__main__':
    print(fetch_updates_data())  # <-- This will print the update data
    app.run(debug=True)
