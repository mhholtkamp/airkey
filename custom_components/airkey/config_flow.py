import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

DOMAIN = "airkey"
CONF_API_KEY = "api_key"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = 15

@config_entries.HANDLERS.register(DOMAIN)
class AirKeyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AirKey."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            api_key = user_input.get(CONF_API_KEY)
            scan_interval = user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

            return self.async_create_entry(
                title="Evva Airkey",
                data={
                    CONF_API_KEY: api_key,
                    CONF_SCAN_INTERVAL: scan_interval,
                }
            )

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
                vol.Coerce(int), vol.Range(min=1)
            ),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            title="Evva Airkey API Key",
        )
