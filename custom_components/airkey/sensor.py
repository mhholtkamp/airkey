from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from datetime import timedelta
import logging
import requests

from .const import DOMAIN, DEFAULT_REFRESH_RATE

_LOGGER = logging.getLogger(__name__)

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
    """Set up Evva Airkey sensors based on a config entry."""
    coordinator = AirkeyDataUpdateCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(AirkeySensor(coordinator, sensor_type))

    async_add_entities(entities)

class AirkeyDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Evva Airkey data from API."""

    def __init__(self, hass, config_entry):
        """Initialize the coordinator."""
        self.api_key = config_entry.data[CONF_API_KEY]
        self.refresh_rate = config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_REFRESH_RATE)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=self.refresh_rate),
        )

    async def _async_update_data(self):
        """Fetch data from the Airkey API."""
        try:
            data = {}
            session = requests.Session()
            session.headers.update({"X-API-Key": self.api_key})

            for sensor in SENSOR_TYPES:
                url = f"https://api.airkey.evva.com:443/cloud/v1/{sensor.replace('_', '-')}"
                response = session.get(url)
                response.raise_for_status()
                data[sensor] = response.json()

            return data

        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")

class AirkeySensor(CoordinatorEntity, SensorEntity):
    """Representation of a sensor entity."""

    def __init__(self, coordinator, sensor_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.sensor_type = sensor_type
        self._attr_name = SENSOR_TYPES[sensor_type]
        self._attr_unique_id = f"{DOMAIN}_{sensor_type}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.sensor_type)

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        attributes = {}
        if self.sensor_type == "events":
            # example for adding custom attributes
            for event in self.coordinator.data.get("events", []):
                event_id = event.get("lockid")
                if event_id:
                    lock = next((lock for lock in self.coordinator.data.get("locks", []) if lock.get("id") == event_id), {})
                    event["lockDoor"] = lock.get("lockDoor")
            attributes["events"] = self.coordinator.data.get("events", [])

        return attributes
