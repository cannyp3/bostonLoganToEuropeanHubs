import requests
from datetime import datetime
import os


# Get API key from environment
API_KEY = os.environ.get('AVIATIONSTACK_API_KEY')
if not API_KEY:
    raise ValueError("No API key found in AVIATIONSTACK_API_KEY environment variable")

API_URL = 'http://api.aviationstack.com/v1/flights'

# Get today's date in YYYY-MM-DD format
today = datetime.now().strftime('%Y-%m-%d')
destinations = ['LHR','FRA','AMS'] # London, Frankfurt, Amsterdam
all_flights = []

try: 
    for dest in destinations:
        params = {
        'access_key': API_KEY,
        'dep_iata': 'BOS',
        'arr_iata': dest, 
        'flight_status': 'scheduled',
        'limit': 100,
        'dep_scheduled_time_min': f'{today}T05:00:00',  # 5 AM
        'dep_scheduled_time_max': f'{today}T23:00:00'   # 11 PM
        }

        response = requests.get(API_URL, params=params)
        data = response.json()
        for flight in data.get('data', []):
            departure_time = flight.get('departure',{}).get('scheduled','')
            all_flights.append({
                'time': departure_time.split('T')[1][:5] if departure_time else 'N/A',
                'number': flight.get('flight', {}).get('iata', ''),
                'destination': flight.get('arrival', {}).get('iata', ''),
                'airline': flight.get('airline', {}).get('name', '')
            })
        
    all_flights.sort(key=lambda x: x['time'])

    # Generate HTML
    html = f"""<html>
    <head>
        <title>Weekend European Hub Departures from Boston</title>
        <link rel="stylesheet" href="styles.css">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <h1> Departures to European Hubs from Boston Today</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>"""

    if all_flights: 
        html += """
        <table>
            <tr>
                <th>Departure Time</th>
                <th>Flight Number</th>
                <th>Destination</th>
                <th>Airline</th>
            </tr>"""
        
        for flight in all_flights:
            html += f"""
            <tr>
                <td>{flight['time']}</td>
                <td>{flight['number']}</td>
                <td>{flight['destination']}</td>
                <td>{flight['airline']}</td>
            </tr>"""
        
        html += "</table>"
    else:
        html += """
        <div class="no-flights">
            <p>No aircraft departing from Logan Airport to European hubs today.</p>
        </div>"""
    
    html += """
    </body>
    </html>"""

    with open("index.html", "w") as f:
        f.write(html)
    print("HTML file generated successfully")

except Exception as e:
    print(f"Error: {e}")
