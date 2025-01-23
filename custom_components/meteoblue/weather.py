import logging
import aiohttp
from datetime import datetime, timedelta

from homeassistant.components.weather import (
    WeatherEntity,
    Forecast,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TEMP_LOW,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_PRECIPITATION_PROBABILITY,
)
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPressure,
    UnitOfSpeed,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=30)  # Poll every 30 minutes

async def async_setup_entry(hass, config_entry, async_add_entities):
    api_key = config_entry.data["api_key"]
    lat = config_entry.data["latitude"]
    lon = config_entry.data["longitude"]
    async_add_entities([MeteoblueWeather(api_key, lat, lon)], True)

class MeteoblueWeather(WeatherEntity):
    def __init__(self, api_key, lat, lon):
        self._api_key = api_key
        self._lat = lat
        self._lon = lon
        self._data = None
        self._last_update = None

    async def async_update(self):
        # Skip update if within scan interval
        if self._last_update and datetime.now() - self._last_update < SCAN_INTERVAL:
            _LOGGER.debug("Skipping update; within scan interval")
            return

        url = f"https://my.meteoblue.com/packages/basic-1h_basic-day?apikey={self._api_key}&lat={self._lat}&lon={self._lon}&format=json"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Failed to fetch data from Meteoblue API: {response.status}")
                        self._data = None
                        return

                    self._data = await response.json()
                    _LOGGER.debug(f"Fetched data from Meteoblue: {self._data}")

                    # Ensure required keys exist in the response
                    if "data_1h" not in self._data or "temperature" not in self._data["data_1h"]:
                        _LOGGER.error("Meteoblue API response is missing required keys")
                        self._data = None
                        return

                    self._last_update = datetime.now()

        except Exception as e:
            _LOGGER.error(f"Error updating Meteoblue data: {e}")
            self._data = None

    @property
    def name(self):
        return f"Weather {self._lat}, {self._lon}"

    @property
    def native_temperature(self):
        if self._data and "data_1h" in self._data and "temperature" in self._data["data_1h"]:
            return self._data["data_1h"]["temperature"][0]
        return None

    @property
    def native_temperature_unit(self):
        return UnitOfTemperature.CELSIUS

    @property
    def native_pressure(self):
        if self._data and "data_1h" in self._data and "sealevelpressure" in self._data["data_1h"]:
            return self._data["data_1h"]["sealevelpressure"][0]
        return None

    @property
    def native_pressure_unit(self):
        return UnitOfPressure.HPA

    @property
    def native_wind_speed(self):
        if self._data and "data_1h" in self._data and "windspeed" in self._data["data_1h"]:
            return self._data["data_1h"]["windspeed"][0]
        return None

    @property
    def native_wind_speed_unit(self):
        return UnitOfSpeed.METERS_PER_SECOND

    @property
    def humidity(self):
        if self._data and "data_1h" in self._data and "relativehumidity" in self._data["data_1h"]:
            return self._data["data_1h"]["relativehumidity"][0]
        return None

    @property
    def wind_bearing(self):
        if self._data and "data_1h" in self._data and "winddirection" in self._data["data_1h"]:
            return self._data["data_1h"]["winddirection"][0]
        return None

    @property
    def forecast(self):
        if not self._data or "data_day" not in self._data:
            return None

        forecast_data = []
        for i, time in enumerate(self._data["data_day"]["time"]):
            try:
                forecast_data.append({
                    ATTR_FORECAST_TIME: time,
                    ATTR_FORECAST_TEMP: self._data["data_day"]["temperature_max"][i],
                    ATTR_FORECAST_TEMP_LOW: self._data["data_day"]["temperature_min"][i],
                    ATTR_FORECAST_PRECIPITATION: self._data["data_day"]["precipitation"][i],
                    ATTR_FORECAST_PRECIPITATION_PROBABILITY: self._data["data_day"]["precipitation_probability"][i],
                })
            except IndexError:
                _LOGGER.warning(f"Forecast data incomplete for index {i}")
                continue
        return forecast_data
