from homeassistant.helpers.entity import Entity

from .const import DOMAIN

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Airkey sensor platform."""
    coordinator = hass.data[DOMAIN]["coordinator"]
    async_add_entities([AirkeySensor(coordinator)], True)

class AirkeySensor(Entity):
    """Representation of an Airkey sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_name = "Airkey Events"
        self._attr_unique_id = "airkey_events"
        self._attr_device_class = "event"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("events")

    @property
    def available(self):
        """Return if the entity is available."""
        return self.coordinator.last_update_success
