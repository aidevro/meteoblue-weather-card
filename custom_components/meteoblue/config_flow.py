# custom_components/meteoblue/config_flow.py

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE
import voluptuous as vol

class MeteoblueConfigFlow(config_entries.ConfigFlow, domain="meteoblue"):
    VERSION = 1
    
    async def async_step_user(self, user_input=None):
        errors = {}
        
        if user_input is not None:
            return self.async_create_entry(
                title="Meteoblue Weather",
                data={
                    CONF_API_KEY: user_input[CONF_API_KEY],
                    CONF_LATITUDE: user_input[CONF_LATITUDE],
                    CONF_LONGITUDE: user_input[CONF_LONGITUDE],
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_LATITUDE): float,
                vol.Required(CONF_LONGITUDE): float,
            }),
            errors=errors,
        )