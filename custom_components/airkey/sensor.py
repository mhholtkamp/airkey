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

        data, attributes = await self.fetch_data()

        # Hier plaatsen we een korte waarde in de state, zoals de lengte van de events
        if data:
            self._state = len(data) if isinstance(data, list) else "OK"
            self._attributes = attributes

    async def fetch_data(self):
        """Helper function to perform the API request."""
        url = self._get_api_url()

        headers = {
            "X-API-Key": self._api_key,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    _LOGGER.debug(f"Fetched data for {self._name}: {data}")

                    # Hier plaatsen we de data in attributes in plaats van direct in state
                    attributes = {"raw_data": data}
                    return data, attributes
                else:
                    _LOGGER.error(f"Error fetching data from {url}, status: {response.status}")
                    return None, {}

    def _get_api_url(self):
        """Construct the correct API URL based on the sensor type."""
        base_url = "https://api.airkey.evva.com:443/cloud/v1/"
        endpoints = {
            "events": f"{base_url}events?createdAfter=2024-08-01T09:15:10.295Z&limit=1000",
            "credits": f"{base_url}credits",
            # Voeg hier de andere endpoints toe
        }
        return endpoints.get(self._type, base_url)
