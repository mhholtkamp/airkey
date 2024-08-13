from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

from .const import DOMAIN, CONF_API_KEY, CONF_SCAN_INTERVAL

class AirkeyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Airkey."""

    VERSION = 1

    def __init__(self):
        """Initialize the flow."""
        self._api_key = None
        self._scan_interval = 15

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            self._api_key = user_input[CONF_API_KEY]
            self._scan_interval = user_input.get(CONF_SCAN_INTERVAL, 15)

            return self.async_create_entry(
                title="Airkey Integration",
                data={
                    CONF_API_KEY: self._api_key,
                    CONF_SCAN_INTERVAL: self._scan_interval,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Optional(CONF_SCAN_INTERVAL, default=15): int,
                }
            ),
        )
