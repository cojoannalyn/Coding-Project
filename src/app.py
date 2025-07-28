from flask import Flask, render_template_string, request

app = Flask(__name__)

landing_html = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Plan Smarter. Travel Further.</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: #f8fafd; }
    .hero { background: linear-gradient(90deg, #f7c6e0 0%, #b3d8f7 100%); padding: 40px 0 0 0; text-align: center; position: relative; }
    .hero h1 { font-size: 2.5rem; color: #222; margin-bottom: 20px; font-weight: 700; }
    .hero img { width: 120px; position: absolute; right: 10%; top: 30px; }
    .start-btn { background: #fff; color: #222; font-weight: 600; border: none; border-radius: 8px; padding: 14px 32px; font-size: 1.1rem; cursor: pointer; box-shadow: 0 2px 8px #0001; margin-top: 20px; transition: background 0.2s; }
    .start-btn:hover { background: #e6f0fa; }
    .features { display: flex; justify-content: space-around; background: #fff; padding: 40px 0; margin-top: -10px; box-shadow: 0 2px 8px #0001; }
    .feature { text-align: center; width: 30%; }
    .feature-icon { font-size: 2.5rem; margin-bottom: 10px; color: #4a90e2; }
    .feature-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 8px; }
    @media (max-width: 700px) {
      .features { flex-direction: column; }
      .feature { width: 100%; margin-bottom: 30px; }
      .hero img { position: static; width: 80px; margin-top: 20px; }
    }
  </style>
</head>
<body>
  <div class="hero">
    <h1>Plan Smarter.<br>Travel Further.</h1>
    <form action="/plan" method="get">
      <button class="start-btn" type="submit">Start Planning</button>
    </form>
    <img src="https://img.icons8.com/ios-filled/100/000000/airplane-take-off.png" alt="Airplane" />
  </div>
  <div class="features">
    <div class="feature">
      <div class="feature-icon">💵</div>
      <div class="feature-title">Enter your budget</div>
    </div>
    <div class="feature">
      <div class="feature-icon">🗺️</div>
      <div class="feature-title">Choose destination</div>
    </div>
    <div class="feature">
      <div class="feature-icon">💡</div>
      <div class="feature-title">Get smart deals</div>
    </div>
  </div>
</body>
</html>
'''

results_html = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Travel Options</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; background: #f8fafd; margin: 0; }
    .results-container {
      max-width: 600px;
      margin: 40px auto 0 auto;
      background: #fff;
      border-radius: 18px;
      box-shadow: 0 4px 24px #0002;
      padding: 36px 32px 28px 32px;
      text-align: center;
    }
    .results-container h2 {
      color: #2d3a4a;
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 18px;
    }
    .summary {
      background: #eaf4fb;
      border-radius: 10px;
      padding: 18px 0 10px 0;
      margin-bottom: 28px;
      font-size: 1.1rem;
      color: #357ab8;
      font-weight: 500;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-around;
      gap: 10px;
    }
    .summary span { display: block; min-width: 120px; }
    .section-title {
      color: #4a90e2;
      font-size: 1.2rem;
      font-weight: 600;
      margin: 18px 0 10px 0;
      letter-spacing: 0.5px;
    }
    .options-list {
      list-style: none;
      padding: 0;
      margin: 0 0 18px 0;
    }
    .options-list li {
      background: #f4f8fb;
      margin-bottom: 10px;
      border-radius: 7px;
      padding: 14px 18px;
      color: #222;
      font-size: 1.05rem;
      box-shadow: 0 1px 4px #4a90e210;
      text-align: left;
      display: flex;
      align-items: center;
      gap: 10px;
      justify-content: space-between;
    }
    .options-list li:before {
      content: '✈️';
      font-size: 1.2rem;
      color: #4a90e2;
      margin-right: 8px;
      display: inline-block;
    }
    .hotel-list li:before {
      content: '🏨';
      color: #4a90e2;
    }
    .book-btn {
      background: linear-gradient(90deg, #4a90e2 0%, #b3d8f7 100%);
      color: #fff;
      font-weight: 600;
      border: none;
      border-radius: 7px;
      padding: 8px 18px;
      font-size: 1rem;
      cursor: pointer;
      box-shadow: 0 1px 4px #4a90e220;
      transition: background 0.2s;
      margin-left: 10px;
    }
    .book-btn:hover {
      background: linear-gradient(90deg, #357ab8 0%, #7fc1f9 100%);
    }
    .plan-again-btn {
      display: inline-block;
      margin-top: 18px;
      background: linear-gradient(90deg, #4a90e2 0%, #b3d8f7 100%);
      color: #fff;
      font-weight: 700;
      border: none;
      border-radius: 7px;
      padding: 12px 32px;
      font-size: 1.1rem;
      cursor: pointer;
      box-shadow: 0 2px 8px #4a90e220;
      transition: background 0.2s;
      text-decoration: none;
    }
    .plan-again-btn:hover {
      background: linear-gradient(90deg, #357ab8 0%, #7fc1f9 100%);
    }
    @media (max-width: 700px) {
      .results-container { padding: 18px 6vw; }
      .summary { flex-direction: column; align-items: center; }
    }
  </style>
</head>
<body>
  <div class="results-container">
    <h2>Recommended Flights & Hotels</h2>
    <div class="summary">
      <span><b>Budget:</b> ${{ budget }}</span>
      <span><b>From:</b> {{ origin }}</span>
      <span><b>To:</b> {{ destination }}</span>
      <span><b>Duration:</b> {{ duration }} days</span>
    </div>
    <div class="section-title">Flight Options</div>
    <ul class="options-list" id="flight-list">
      {% for flight in flights %}
        {% set price = (flight.split('$')[-1].replace(')','').replace(',','').strip()) %}
        <li>
          <input type="radio" name="flightOption" value="{{ price }}" data-label="{{ flight }}" id="flight{{ loop.index }}">
          <label for="flight{{ loop.index }}">{{ flight }}</label>
          <button class="book-btn" onclick="showTotal('Flight', '{{ flight }}', {{ price }}, {{ duration }})">Book This!</button>
        </li>
      {% endfor %}
    </ul>
    <div class="section-title">Hotel Options</div>
    <ul class="options-list hotel-list" id="hotel-list">
      {% for hotel in hotels %}
        {% set price = (hotel.split('$')[-1].split('/')[0].replace(')','').replace(',','').strip()) %}
        <li>
          <input type="radio" name="hotelOption" value="{{ price }}" data-label="{{ hotel }}" id="hotel{{ loop.index }}">
          <label for="hotel{{ loop.index }}">{{ hotel }}</label>
          <button class="book-btn" onclick="showTotal('Hotel', '{{ hotel }}', {{ price }}, {{ duration }})">Book This!</button>
        </li>
      {% endfor %}
    </ul>
    <button class="plan-again-btn" style="margin-top:30px;" onclick="calcTripTotal({{ duration }})">Total Trip Cost</button>
    <a href="/" class="plan-again-btn" style="margin-left:10px;">Plan another trip</a>
  </div>
  <script>
    function showTotal(type, name, price, duration) {
      let total = price;
      if(type === 'Hotel') {
        total = price * duration;
      }
      alert(`Booking for: ${name}\nTotal cost: $${total}`);
    }

    function calcTripTotal(duration) {
      // Get selected flight
      const flightRadio = document.querySelector('input[name="flightOption"]:checked');
      const hotelRadio = document.querySelector('input[name="hotelOption"]:checked');
      if (!flightRadio || !hotelRadio) {
        alert('Please select both a flight and a hotel option.');
        return;
      }
      const flightLabel = flightRadio.getAttribute('data-label');
      const hotelLabel = hotelRadio.getAttribute('data-label');
      const flightCost = parseFloat(flightRadio.value);
      const hotelCost = parseFloat(hotelRadio.value) * duration;
      const total = flightCost + hotelCost;
      alert(`Total Trip Cost\n\nFlight: ${flightLabel}\nHotel: ${hotelLabel}\n\nTotal: $${total}`);
    }
  </script>
</body>
</html>
'''

# Landing page
@app.route('/', methods=['GET'])
def landing():
    return render_template_string(landing_html)

# Planning form and results (existing logic)
form_html = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Plan Your Trip</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; background: #f8fafd; margin: 0; }
    .form-container {
      max-width: 400px;
      margin: 60px auto 0 auto;
      background: #fff;
      border-radius: 18px;
      box-shadow: 0 4px 24px #0002;
      padding: 36px 32px 28px 32px;
      text-align: center;
    }
    .form-container h2 {
      margin-bottom: 24px;
      color: #2d3a4a;
      font-size: 2rem;
      font-weight: 700;
    }
    .input-group {
      margin-bottom: 18px;
      text-align: left;
    }
    .input-group label {
      display: block;
      margin-bottom: 6px;
      color: #4a90e2;
      font-weight: 600;
    }
    .input-group input, .input-group select {
      width: 100%;
      padding: 10px 12px;
      border: 1px solid #c3d0e0;
      border-radius: 7px;
      font-size: 1rem;
      background: #f4f8fb;
      transition: border 0.2s;
    }
    .input-group input:focus, .input-group select:focus {
      border: 1.5px solid #4a90e2;
      outline: none;
      background: #fff;
    }
    .submit-btn {
      width: 100%;
      background: linear-gradient(90deg, #4a90e2 0%, #b3d8f7 100%);
      color: #fff;
      font-weight: 700;
      border: none;
      border-radius: 7px;
      padding: 14px 0;
      font-size: 1.1rem;
      cursor: pointer;
      margin-top: 10px;
      box-shadow: 0 2px 8px #4a90e220;
      transition: background 0.2s;
    }
    .submit-btn:hover {
      background: linear-gradient(90deg, #357ab8 0%, #7fc1f9 100%);
    }
    @media (max-width: 500px) {
      .form-container { padding: 18px 6vw; }
    }
  </style>
  <script>
    // Simple country-city mapping for demo
    const countryCities = {
      'USA': ['New York', 'Los Angeles', 'Chicago'],
      'UK': ['London', 'Manchester', 'Edinburgh'],
      'Japan': ['Tokyo', 'Osaka', 'Kyoto'],
      'Australia': ['Sydney', 'Melbourne', 'Brisbane']
    };
    function updateCities(countrySelectId, citySelectId) {
      const country = document.getElementById(countrySelectId).value;
      const citySelect = document.getElementById(citySelectId);
      citySelect.innerHTML = '';
      if (countryCities[country]) {
        countryCities[country].forEach(city => {
          const opt = document.createElement('option');
          opt.value = city;
          opt.text = city;
          citySelect.appendChild(opt);
        });
      } else {
        const opt = document.createElement('option');
        opt.value = '';
        opt.text = 'Select country first';
        citySelect.appendChild(opt);
      }
    }
  </script>
</head>
<body>
  <div class="form-container">
    <h2>Plan Your Trip</h2>
    <form method="post">
      <div class="input-group">
        <label for="budget">Budget ($)</label>
        <input type="number" id="budget" name="budget" min="1" required placeholder="e.g. 1000">
      </div>
      <div class="input-group">
        <label for="origin_country">From Country</label>
        <select id="origin_country" name="origin_country" required onchange="updateCities('origin_country','origin_city')">
          <option value="">Select country</option>
          <option value="USA">USA</option>
          <option value="UK">UK</option>
          <option value="Japan">Japan</option>
          <option value="Australia">Australia</option>
        </select>
      </div>
      <div class="input-group">
        <label for="origin_city">From City</label>
        <select id="origin_city" name="origin_city" required>
          <option value="">Select country first</option>
        </select>
      </div>
      <div class="input-group">
        <label for="destination_country">To Country</label>
        <select id="destination_country" name="destination_country" required onchange="updateCities('destination_country','destination_city')">
          <option value="">Select country</option>
          <option value="USA">USA</option>
          <option value="UK">UK</option>
          <option value="Japan">Japan</option>
          <option value="Australia">Australia</option>
        </select>
      </div>
      <div class="input-group">
        <label for="destination_city">To City</label>
        <select id="destination_city" name="destination_city" required>
          <option value="">Select country first</option>
        </select>
      </div>
      <div class="input-group">
        <label for="duration">Duration (days)</label>
        <input type="number" id="duration" name="duration" min="1" required placeholder="e.g. 7">
      </div>
      <button class="submit-btn" type="submit">Find Options</button>
    </form>
  </div>
  <script>
    // Initialize city dropdowns if country is preselected (for browser autofill)
    document.addEventListener('DOMContentLoaded', function() {
      updateCities('origin_country','origin_city');
      updateCities('destination_country','destination_city');
    });
  </script>
</body>
</html>
'''

@app.route('/plan', methods=['GET', 'POST'])
def plan():
    if request.method == 'POST':
        budget = request.form['budget']
        origin_country = request.form['origin_country']
        origin_city = request.form['origin_city']
        destination_country = request.form['destination_country']
        destination_city = request.form['destination_city']
        duration = request.form['duration']
        origin = f"{origin_city}, {origin_country}"
        destination = f"{destination_city}, {destination_country}"
        # Mock data for demonstration
        flights = [
            f"Fly from {origin} to {destination} on Airline A ($200)",
            f"Fly from {origin} to {destination} on Airline B ($250)"
        ]
        hotels = [
            f"Hotel X near {destination} ($80/night)",
            f"Hotel Y downtown {destination} ($120/night)"
        ]
        return render_template_string(results_html, budget=budget, origin=origin, destination=destination, duration=duration, flights=flights, hotels=hotels)
    return render_template_string(form_html)
