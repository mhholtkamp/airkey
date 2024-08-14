import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from .const import DOMAIN, DEFAULT_REFRESH_RATE

class AirkeyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Evva Airkey."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Hier zou je eventueel validatie van de API-key kunnen uitvoeren
            return self.async_create_entry(title="Evva Airkey", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_REFRESH_RATE): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "api_key_desc": "Enter your Evva API key",
                "scan_interval_desc": "Set the refresh interval in minutes (default: 15)",
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return AirkeyOptionsFlowHandler(config_entry)


class AirkeyOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for Evva Airkey."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle the options step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Optional(CONF_SCAN_INTERVAL, default=self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_REFRESH_RATE)): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=options_schema,
            description_placeholders={
                "scan_interval_desc": "Set the refresh interval in minutes (default: 15)",
            }
        )
