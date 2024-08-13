import logging
import requests
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, SENSOR_NAME, API_URL

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the AirKey sensor platform."""
    api_key = config[CONF_API_KEY]

    coordinator = AirKeyDataUpdateCoordinator(hass, api_key)

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([AirKeySensor(coordinator)], True)


class AirKeyDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the AirKey API."""

    def __init__(self, hass, api_key):
        """Initialize the coordinator."""
        self.api_key = api_key
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from AirKey API."""
        headers = {"X-API-Key": self.api_key}
        try:
            response = requests.get(API_URL, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            _LOGGER.error(f"HTTP error occurred: {http_err}")
            raise UpdateFailed(f"HTTP error: {http_err}")
        except Exception as err:
            _LOGGER.error(f"Error fetching data: {err}")
            raise UpdateFailed(f"Error fetching data: {err}")


class AirKeySensor(SensorEntity):
    """Representation of the AirKey sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator

    @property
    def name(self):
        """Return the name of the sensor."""
        return SENSOR_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
        # Assuming the API returns a list of events
        events = self.coordinator.data.get('events', [])
        return len(events)

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "events": self.coordinator.data.get('events', [])
        }

    async def async_update(self):
        """Update the sensor state."""
        await self.coordinator.async_request_refresh()
