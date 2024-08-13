# Evva Airkey (custom) Integration for Home Assistant

## Overview

This custom component integrates Evva Airkey API with Home Assistant. It allows you to monitor the status of your Airkey locks and users.

## Installation

1. **Add the custom repository to HACS:**
   - Go to HACS in your Home Assistant UI.
   - Click on "Custom repositories" under "Integrations".
   - Add the repository URL: `https://github.com/yourusername/airkey`.
   - Choose "Integration" as the category and click "Add".

2. **Install the custom component:**
   - Go to HACS > Integrations.
   - Search for "Evva Airkey (custom)" and install it.

## Configuration

1. **Add the integration:**
   - Go to Configuration > Integrations in Home Assistant.
   - Click the "+" button and search for "Evva Airkey (custom)".
   - Enter your API key and configure the update interval (default is 15 minutes).

2. **Configure via YAML (optional):**
   You can also configure it using YAML if preferred:
   ```yaml
   airkey:
     api_key: YOUR_API_KEY
     scan_interval: 15
