from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import aiohttp
from datetime import timedelta
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AirKey from a config entry."""
    api_key = entry.data[CONF_API_KEY]
    scan_interval = timedelta(minutes=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))

    coordinator = AirKeyDataUpdateCoordinator(
        hass, aiohttp.ClientSession(), api_key, scan_interval
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN] = {entry.entry_id: coordinator}

    await hass.config_entries.async_forward_entry_setup(entry, 'sensor')

    return True

class AirKeyDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching AirKey data from API."""

    def __init__(self, hass: HomeAssistant, session: aiohttp.ClientSession, api_key: str, scan_interval: timedelta):
        """Initialize the data update coordinator."""
        self.api_key = api_key
        self.session = session
        self.url = "https://integration.api.airkey.evva.com:443/cloud/v1/events?limit=100"
        self.headers = {"X-API-Key": self.api_key}

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=scan_interval,
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            async with self.session.get(self.url, headers=self.headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
