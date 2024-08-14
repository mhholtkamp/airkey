from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
import voluptuous as vol

from .const import DOMAIN, DEFAULT_REFRESH_RATE

class AirkeyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Evva Airkey."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self._show_config_form()

        return self.async_create_entry(title="Evva Airkey", data=user_input)

    def _show_config_form(self, errors=None):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_REFRESH_RATE): int,
                }
            ),
            errors=errors or {},
        )

    async def async_step_import(self, import_data):
        """Handle import from configuration.yaml."""
        return await self.async_step_user(user_input=import_data)
