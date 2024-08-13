import aiohttp
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta

class AirKeySensor:
    """Representation of an AirKey Sensor."""

    def __init__(self, hass, entry):
        """Initialize the sensor."""
        self._hass = hass
        self._entry = entry
        self._api_key = entry.data.get('api_key')
        self._scan_interval = timedelta(minutes=entry.data.get('scan_interval', 15))

        self._coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name="airkey_sensor",
            update_method=self._async_update_data,
            update_interval=self._scan_interval,
        )

    async def async_setup(self):
        """Set up the AirKey sensor."""
        await self._coordinator.async_config_entry_first_refresh()

    async def _async_update_data(self):
        """Fetch data from the AirKey API."""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'X-API-Key': self._api_key}
                async with session.get('https://integration.api.airkey.evva.com:443/cloud/v1/events', headers=headers) as response:
                    data = await response.json()
                    return data
        except Exception as e:
            raise UpdateFailed(f"Error communicating with API: {e}")

    @property
    def name(self):
        """Return the name of the sensor."""
        return "AirKey Events"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._coordinator.data

    @property
    def available(self):
        """Return True if the sensor is available."""
        return self._coordinator.last_update_success
