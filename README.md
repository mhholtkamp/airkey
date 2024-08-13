# EVVA AirKey Home Assistant Integration

This integration allows you to connect EVVA AirKey with Home Assistant to monitor events.

## Installation via HACS

1. Add this repository to HACS as a custom repository.
2. Search for "EVVA AirKey" in the HACS store.
3. Install the integration.
4. Add the following to your `configuration.yaml`:

```yaml
sensor:
  - platform: airkey
    api_key: YOUR_API_KEY
```
