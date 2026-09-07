from odoo import models, fields, api
import meteomatics.api as meteomatics_api
import datetime as dt
import logging

_logger = logging.getLogger(__name__)

class WeatherData(models.Model):
    _name = 'weather.data'
    _description = 'Weather Data'

    location = fields.Char(string='Location')
    temperature = fields.Float(string='Temperature')
    condition = fields.Char(string='Condition', default='Clear')

    def fetch_and_store_weather_data(self):
        # Fetch weather data from the Meteomatics API
        weather_data = self._fetch_weather_data()
        if weather_data:
            # Log the data to be created
            print(f"Creating record with data: {weather_data}")
            # Create a new record with the fetched data
            self.create({
                'location': weather_data['location'],
                'temperature': weather_data['temperature'],
                'condition': weather_data['condition']
            })

    def _fetch_weather_data(self):
        # Meteomatics API credentials
        username = 'odooistic_rajput_farooq'
        password = '7HRQ9smnz9'

        coordinates = [(51.5073219, -0.1276474)]  # London coordinates
        parameters = ['t_2m:C']  # Temperature at 2 meters
        model = 'mix'

        # Set start and end date for the request
        startdate = dt.datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        enddate = startdate + dt.timedelta(hours=1)  # Forecast for the next hour
        interval = dt.timedelta(hours=1)

        try:
            # Query the time series from Meteomatics
            df = meteomatics_api.query_time_series(coordinates, startdate, enddate, interval, parameters, username, password, model=model)
            
            # Log the entire response to check its structure
            print(f"API response: {df}")

            # Parse the temperature value from the DataFrame
            temperature = df['t_2m:C'].iloc[0]  # Correct way to access column data by column name and row index

            # Log the extracted temperature to verify it's correct
            print(f"Extracted temperature: {temperature}")

            return {
                'temperature': temperature,
                'location': 'London',
                'condition': 'Clear'  # Default to 'Clear'
            }
        except Exception as e:
            _logger.error(f"Error fetching weather data: {str(e)}")
            return None


