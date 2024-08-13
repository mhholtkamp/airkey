import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_API_KEY

_LOGGER = logging.getLogger(__name__)

class AirKeyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AirKey integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the user input
            api_key = user_input[CONF_API_KEY]
            if self._validate_api_key(api_key):
                return self.async_create_entry(
                    title="EVVA AirKey",
                    data={CONF_API_KEY: api_key}
                )
            else:
                errors["base"] = "invalid_api_key"

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY): str
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    def _validate_api_key(self, api_key: str) -> bool:
        """Validate the API key."""
        # Here you could add logic to validate the API key with a simple request to the AirKey API
        # For now, we'll assume it's valid
        return True

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow for this handler."""
        return AirKeyOptionsFlow(config_entry)


class AirKeyOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for the integration."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_API_KEY, default=self.config_entry.data.get(CONF_API_KEY)): str
        })

        return self.async_show_form(step_id="init", data_schema=data_schema)
