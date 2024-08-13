"""The Airkey integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import aiohttp
import async_timeout
from datetime import timedelta

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the Airkey integration."""
    api_key = entry.data["api_key"]
    scan_interval = entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)

    coordinator = AirkeyDataUpdateCoordinator(hass, api_key, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, ["sensor"])

    return True

class AirkeyDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, api_key: str, scan_interval: int):
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=scan_interval),
        )
        self.api_key = api_key

    async def _async_update_data(self):
        """Fetch data from the API."""
        url = "https://api.example.com/airkey/status"
        headers = {
            "X-API-Key": self.api_key
        }

        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession().get(url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
