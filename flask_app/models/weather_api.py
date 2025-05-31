from flask import request, session, redirect, flash, render_template
from flask import current_app # To access app.config
from flask.config import Config
from flask import config
from flask_app.models import user, group, event, discussion, message

def get_nws_forecast(latitude, longitude):
    print('"you made it to th def get_nws_forecast under weather_api in models.')
    """
    Fetches the weather forecast from the NWS API for a given lat/lon.
    """
    headers = {
        'User-Agent': current_app.config['NWS_API_USER_AGENT'],
        'Accept': 'application/geo+json' # NWS API often uses geo+json
    }
    points_url = f"{current_app.config['NWS_API_BASE_URL']}/points/{latitude},{longitude}"

    try:
        # Step 1: Get the forecast grid URL
        points_response = request.get(points_url, headers=headers, timeout=10)
        points_response.raise_for_status()  # Raise an exception for HTTP errors
        points_data = points_response.json()

        forecast_url = points_data.get('properties', {}).get('forecast')
        hourly_forecast_url = points_data.get('properties', {}).get('forecastHourly')
        # You can also get forecastOffice, gridX, gridY if needed for other calls

        if not forecast_url:
            return None, "Could not retrieve forecast URL from NWS points endpoint."

        # Step 2: Get the actual forecast using the forecast URL
        forecast_response = request.get(forecast_url, headers=headers, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # You might want to process/simplify forecast_data['properties']['periods']
        # For now, we'll return the relevant part
        return forecast_data.get('properties', {}), None

    except request.exceptions.RequestException as e:
        current_app.logger.error(f"NWS API request failed: {e}")
        return None, str(e)
    except (KeyError, TypeError) as e:
        current_app.logger.error(f"Error parsing NWS API response: {e}")
        return None, "Error parsing NWS API response."