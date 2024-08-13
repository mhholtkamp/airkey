from .const import DOMAIN

async def async_setup(hass, config):
    """Setup the AirKey integration."""
    hass.data.setdefault(DOMAIN, {})
    return True
