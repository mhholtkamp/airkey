from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .sensor import AirKeySensor

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the AirKey component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AirKey from a config entry."""
    hass.data.setdefault('airkey', {})
    
    # Create the sensor instance and store it in the hass.data dictionary
    hass.data['airkey'][entry.entry_id] = AirKeySensor(hass, entry)

    # Setup the sensor
    await hass.data['airkey'][entry.entry_id].async_setup()

    return True
