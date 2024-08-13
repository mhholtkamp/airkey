import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, CONF_API_KEY

@config_entries.HANDLERS.register(DOMAIN)
class AirKeyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AirKey."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the API key or perform any setup checks here
            api_key = user_input.get(CONF_API_KEY)

            # Example validation check
            if not api_key:
                errors["base"] = "invalid_api_key"
            else:
                # Perform a test with the API key
                try:
                    # Add your API key validation logic here
                    return self.async_create_entry(title="Evva Airkey", data=user_input)
                except Exception as e:
                    # Log exception and show error
                    _LOGGER.error(f"API Key validation failed: {e}")
                    errors["base"] = "api_key_error"

        # Define the schema for the form
        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            title="Evva Airkey API-key",  # Title to show on the form
        )
