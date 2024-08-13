import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SENSOR_NAME, API_URL, CONF_API_KEY

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the AirKey sensor from a config entry."""
    api_key = config_entry.data[CONF_API_KEY]

    coordinator = AirKeyDataUpdateCoordinator(hass, api_key)

    await coordinator.async_config_entry_first_refresh()
    
    # Voeg debug logging toe
    _LOGGER.debug("Adding AirKey sensor entity")
    
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

        async with aiohttp.ClientSession() as session:
            try:
                with async_timeout.timeout(10):
                    async with session.get(API_URL, headers=headers) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"Unexpected status code: {response.status}")
                        data = await response.json()
                        _LOGGER.debug("Fetched data: %s", data)
                        return data

            except aiohttp.ClientError as err:
                _LOGGER.error(f"Error fetching data: {err}")
                raise UpdateFailed(f"Error fetching data: {err}")



class AirKeySensor(SensorEntity):
    """Representation of the AirKey sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_unique_id = "airkey_events"

    @property
    def name(self):
        """Return the name of the sensor."""
        return SENSOR_NAME

    @property
    def state(self):
        """Return the state of the sensor."""
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

