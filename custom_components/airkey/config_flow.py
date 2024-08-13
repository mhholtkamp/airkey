"""Config flow for the Airkey integration."""

from typing import Any, Dict
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from .const import DOMAIN

class AirkeyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Airkey."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self.api_key = None
        self.scan_interval = None

    async def async_step_user(self, user_input: Dict[str, Any] = None):
        """Handle the initial step."""
        if user_input is not None:
            self.api_key = user_input[CONF_API_KEY]
            self.scan_interval = user_input.get(CONF_SCAN_INTERVAL, 15)
            return self.async_create_entry(
                title="Airkey",
                data={
                    CONF_API_KEY: self.api_key,
                },
                options={
                    CONF_SCAN_INTERVAL: self.scan_interval,
                },
            )
        return self.async_show_form(
            step_id="user",
            data_schema=self._get_schema(),
        )

    def _get_schema(self):
        """Return the schema for user input."""
        return vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=15): int,
            }
        )
