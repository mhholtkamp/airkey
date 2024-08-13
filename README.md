# airkey
Home assistant custom component to interact with the free Evva Airkey (r/o) api

## Purpose
Create sensors in Home Assistant to retrieve information from the Airkey api.
The free version of the api only supports read only

## What you need
- Evva Airkey account with locks
- Api-key by Evva

## Configuration
Add this to ```configuration.yaml```:
```
sensor:
  - platform: airkey
    api_key: YOUR_API_KEY
```
