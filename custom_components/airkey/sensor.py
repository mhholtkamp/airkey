import logging
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
    api_key = config_entry.data[CONF_API_KEY]
    scan_interval = config_entry.options.get(CONF_SCAN_INTERVAL, 15)

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(AirkeySensor(sensor_type, api_key, scan_interval))

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
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    async def async_update(self):
        """Fetch new state data for the sensor."""
        _LOGGER.debug(f"Updating Airkey sensor: {self._name}")

        # Hier maak je de API-call aan, afhankelijk van het type sensor
        if self._type == "events":
            # Voorbeeld API-call voor events, gebruik aiohttp voor async requests
            self._state, self._attributes = await self.fetch_data("https://api.airkey.evva.com:443/cloud/v1/events?createdAfter=2024-08-01T09:15:10.295Z&limit=1000")
        elif self._type == "credits":
            self._state, self._attributes = await self.fetch_data("https://api.airkey.evva.com:443/cloud/v1/credits")
        # Voeg hier de andere sensors toe

    async def fetch_data(self, url):
        """Helper function to perform the API request."""
        headers = {
            "X-API-Key": self._api_key,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Pas hier aan om de juiste data uit de JSON te halen
                    return data, {}
                else:
                    _LOGGER.error(f"Error fetching data from {url}, status: {response.status}")
                    return None, {}
