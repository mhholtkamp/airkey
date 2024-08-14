from datetime import timedelta
import requests
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_REFRESH_RATE

SENSOR_TYPES = {
    "events": "Events",
    "credits": "Credits",
    "areas": "Areas",
    "maintenance-tasks": "Maintenance Tasks",
    "media": "Media",
    "persons": "Persons",
    "blacklists": "Blacklists",
    "authorizations": "Authorizations",
    "locks": "Locks"
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Evva Airkey sensors."""
    coordinator = AirkeyDataUpdateCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    entities = [AirkeySensor(coordinator, sensor) for sensor in SENSOR_TYPES]
    async_add_entities(entities, True)

class AirkeyDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Airkey API."""

    def __init__(self, hass, config_entry):
        """Initialize."""
        self.api_key = config_entry.data[CONF_API_KEY]
        self.refresh_rate = config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_REFRESH_RATE)
        self.session = requests.Session()
        self.session.headers.update({"X-API-Key": self.api_key})

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=self.refresh_rate),
        )

    async def _async_update_data(self):
        """Update data via API."""
        try:
            data = {}
            for sensor in SENSOR_TYPES:
                endpoint = f"https://api.airkey.evva.com:443/cloud/v1/{sensor.replace('_', '-')}"
                response = self.session.get(endpoint)
                response.raise_for_status()
                data[sensor] = response.json()
            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

class AirkeySensor(SensorEntity):
    """Representation of a Evva Airkey Sensor."""

    def __init__(self, coordinator, sensor_type):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.sensor_type = sensor_type
        self._attr_name = SENSOR_TYPES[sensor_type]
        self._attr_unique_id = f"{DOMAIN}_{sensor_type}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.sensor_type]

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        # Handle custom attributes here based on relationships between entities.
        return {}
