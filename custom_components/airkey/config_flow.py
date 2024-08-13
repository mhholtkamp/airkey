from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

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

            # Here you could validate the API key
            if len(api_key) == 0:  # Example check
                errors["base"] = "invalid_api_key"
            else:
                # If the API key is valid, create the entry
                return self.async_create_entry(title="Evva Airkey", data=user_input)

        # Define the schema for the form
        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str
        })

        # Show the form with a title
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders=None,
            title="Evva Airkey API-key",  # This is where you set the title
        )
