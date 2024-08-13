import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the Airkey integration from a config entry."""
    api_key = entry.data[CONF_API_KEY]
    update_interval = entry.data.get(CONF_SCAN_INTERVAL, 15)

    coordinator = AirkeyDataUpdateCoordinator(
        hass, api_key, timedelta(minutes=update_interval)
    )

    await coordinator.async_refresh()

    hass.data[DOMAIN] = {"coordinator": coordinator}

    # Set up sensors here if needed

    return True

class AirkeyDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Airkey data from API."""

    def __init__(self, hass: HomeAssistant, api_key: str, update_interval: timedelta):
        """Initialize global Airkey data updater."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.api_key = api_key

    async def _async_update_data(self):
        """Fetch data from the Airkey API."""
        try:
            async with self.hass.async_add_executor_job(self._fetch_data) as response:
                return response
        except Exception as e:
            raise UpdateFailed(f"Error communicating with API: {e}")

    def _fetch_data(self):
        import requests

        url = "https://api.evva.com/airkey/events"
        headers = {"X-API-Key": self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
