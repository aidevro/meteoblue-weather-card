"""Support for Meteoblue weather service."""
from datetime import datetime, timedelta
import logging

import meteoblue_api_python
from meteoblue_api_python import MeteoblueClient

from homeassistant.components.weather import (
    WeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.const import (
    CONF_API_KEY,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    UnitOfTemperature,
    UnitOfPressure,
    UnitOfSpeed,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=30)

async def async_setup_entry(
    hass: HomeAssistant, 
    config_entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback
):
    """Set up the Meteoblue weather entity."""
    client = MeteoblueClient(
        api_key=config_entry.data[CONF_API_KEY],
        lat=config_entry.data[CONF_LATITUDE],
        lon=config_entry.data[CONF_LONGITUDE],
    )
    
    async_add_entities([MeteoblueWeather(client)], True)

class MeteoblueWeather(WeatherEntity):
    """Implementation of a Meteoblue weather condition."""

    def __init__(self, client):
        """Initialize the Meteoblue weather."""
        self._client = client
        self._name = "Meteoblue Weather"
        self._data = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"meteoblue_{self._client.lat}_{self._client.lon}"

    @property
    def temperature(self):
        """Return the temperature."""
        if self._data:
            return self._data.get("temperature")
        return None

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return UnitOfTemperature.CELSIUS

    @property
    def humidity(self):
        """Return the humidity."""
        if self._data:
            return self._data.get("humidity")
        return None

    @property
    def pressure(self):
        """Return the pressure."""
        if self._data:
            return self._data.get("pressure")
        return None

    @property
    def wind_speed(self):
        """Return the wind speed."""
        if self._data:
            return self._data.get("wind_speed")
        return None

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        if self._data:
            return self._data.get("wind_bearing")
        return None

    @property
    def attribution(self):
        """Return the attribution."""
        return "Data provided by Meteoblue"

    async def async_update(self):
        """Update current conditions."""
        try:
            data = await self._client.get_current_weather()
            self._data = {
                "temperature": data["temperature"],
                "humidity": data["humidity"],
                "pressure": data["pressure"],
                "wind_speed": data["wind_speed"],
                "wind_bearing": data["wind_bearing"],
            }
        except Exception as err:
            _LOGGER.error("Couldn't fetch Meteoblue data: %s", err)
