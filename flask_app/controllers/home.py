from flask_app import app
from flask import render_template, session, redirect, request, flash, url_for
from flask_app.controllers import users, groups, events, messages, discussions
from flask_app.models.user import User
from flask_app.models.group import Group
from flask_app.models.event import Event
from flask_app.models.discussion import Discussion
from flask_app.models.message import Message
from flask_app.models.weather_api import get_nws_forecast
from flask import Blueprint, jsonify, request, current_app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    if session.get('user_id'):
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect('/')
    user_data = {
        'id' : session.get('user_id')
    }
    team_id = User.get_group_id_by_user_id(user_data)
    session['team_id'] = team_id
    team_data = {
        'id' : session.get('team_id')
    }
    # The below block of code will allow you to check what key value pairs are currently stored in session.
    # session_data = []
    # for key, value in session.items():
    #     session_data.append(f"{key}: {value}")
    # session_contents = "<br>".join(session_data)
    # print('session contents: ', session_contents)
    user = User.get_by_id(user_data)
    event = Event.get_events_by_group(team_data)
    message = Message.get_messages_by_group(team_data)
    return render_template('dashboard.html', user = user, event = event, message = message, team_id = team_id)

@app.route('/weather')
def weather():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('weather.html', user = user)

@app.route('/time')
def time():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('time.html', user = user)

@app.route('/discussion_board')
def discussion_board():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('discussion_board.html', user = user)

@app.route('/photos')
def photos():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('photos.html', user = user)

@app.route('/add_photo')
def add_photo():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('add_photo.html', user = user)

@app.route('/login', methods=["POST"])
def login():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password']
    }
    if not User.validate_user_login(data):
        return redirect('/')
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid Email and/or Password')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email and/or Password')
        return redirect('/')
    session['user_id'] = user_in_db.id
    print(session['user_id'])
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

weather_bp = Blueprint('weather_bp', __name__, url_prefix='/api')

@app.route('/weather_forecast', methods=['GET'])
def weather_endpoint():
    print("you made it to weather_endpoint in home.py under controllers")
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    print("latitude = ", latitude, "longitude = ", longitude)
    # if not latitude or not longitude:
    #     return jsonify({"error": "Missing latitude (lat) or longitude (lon) parameters"}), 400

    # try:
    #     # Validate if lat and lon are numbers if necessary
    #     float(latitude)
    #     float(longitude)
    # except ValueError:
    #     return jsonify({"error": "Latitude and longitude must be valid numbers"}), 400

    current_app.logger.info(f"Fetching weather for lat={latitude}, lon={longitude}")
    forecast_properties, error = get_nws_forecast(latitude, longitude)

    if error:
        return jsonify({"error": f"Could not retrieve weather data: {error}"}), 500

    if forecast_properties and 'periods' in forecast_properties:
        # You might want to return the whole 'periods' array or select specific data
        # For Fahrenheit, you'd look for 'temperatureUnit': 'F' in the periods.
        # The NWS API usually defaults to Fahrenheit if not specified, but always check the 'temperatureUnit'.
        periods = forecast_properties['periods']
        
        # Convert temperatures to Fahrenheit if they are in Celsius
        # (NWS API typically provides Fahrenheit directly for US locations)
        # Example conversion (if needed):
        # for period in periods:
        #     if period.get('temperatureUnit') == 'C':
        #         period['temperature'] = round(period['temperature'] * 9/5 + 32)
        #         period['temperatureUnit'] = 'F'

        return jsonify({
            "latitude": latitude,
            "longitude": longitude,
            "forecast": periods
        }), 200
    else:
        return jsonify({"error": "No forecast data found or unexpected response format."}), 500

# Example of a simple HTML page route (optional)
# This uses the 'templates' folder
@weather_bp.route('/test-page', methods=['GET'])
def test_page():
    from flask import render_template
    # This would render app/templates/index.html
    # You'd create an index.html file in the templates folder
    return render_template('weather_page.html', message="Test page for Weather API")