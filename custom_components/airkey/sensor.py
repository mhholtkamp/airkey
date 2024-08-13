import logging
from datetime import timedelta
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL = timedelta(minutes=15)

# Schema voor configuratie-instellingen
CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL.total_seconds() / 60): vol.All(
            vol.Coerce(int), vol.Range(min=1)
        ),
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AirKey from a config entry."""
    api_key = entry.data[CONF_API_KEY]
    scan_interval = timedelta(minutes=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL.total_seconds() / 60))

    coordinator = AirKeyDataUpdateCoordinator(
        hass, aiohttp.ClientSession(), api_key, scan_interval
    )
    
    # Haal eerst de gegevens op
    await coordinator.async_config_entry_first_refresh()

    # Voeg de sensor toe aan Home Assistant
    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_setup_platform(entry, 'sensor')

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

class AirKeySensor(SensorEntity):
    """Representation of an AirKey sensor."""

    def __init__(self, coordinator: AirKeyDataUpdateCoordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "AirKey Events"
        self._attr_unique_id = "airkey_events"
        self._attr_state = None

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self._attr_state

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        await self.coordinator.async_request_refresh()
        data = self.coordinator.data
        # Verwerk de data en zet de state van de sensor
        self._attr_state = data.get('events', 'No data')
