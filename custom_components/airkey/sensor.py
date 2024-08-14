import logging
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    "events": "Events",
    "credits": "Credits",
    "areas": "Areas",
    "maintenance_tasks": "Maintenance Tasks",
    "media": "Media",
    "persons": "Persons",
    "blacklists": "Blacklists",
    "authorizations": "Authorizations",
    "locks": "Locks",
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Evva Airkey sensors from a config entry."""
    _LOGGER.debug("Setting up Evva Airkey sensors.")
    
    api_key = config_entry.data[CONF_API_KEY]
    scan_interval = config_entry.options.get(CONF_SCAN_INTERVAL, 15)

    entities = []
    for sensor_type in SENSOR_TYPES:
        _LOGGER.debug(f"Creating sensor for {sensor_type}")
        entities.append(AirkeySensor(sensor_type, api_key, scan_interval))

    _LOGGER.debug(f"Adding {len(entities)} sensors.")
    async_add_entities(entities, True)

class AirkeySensor(SensorEntity):
    """Representation of an Evva Airkey sensor."""

    def __init__(self, sensor_type, api_key, scan_interval):
        """Initialize the sensor."""
        self._type = sensor_type
        self._name = SENSOR_TYPES[sensor_type]
        self._state = None
        self._api_key = api_key
        self._scan_interval = scan_interval
        self._attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Airkey {self._name}"

    @property
    def state
