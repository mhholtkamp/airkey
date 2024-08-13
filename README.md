# Airkey Integration for Home Assistant

This is a custom integration for Home Assistant that connects to the Airkey API to provide status updates for your Airkey locks.

## Installation

1. **Via HACS**:
   - Go to HACS in your Home Assistant.
   - Click on "Frontend" or "Integrations".
   - Search for "Airkey".
   - Install the repository.

2. **Manual Installation**:
   - Download the repository as a ZIP file.
   - Extract it and place the `airkey` folder in your Home Assistant `custom_components` directory.

## Configuration

Once installed, add the integration via the Home Assistant UI:

1. Go to Configuration > Integrations.
2. Click on "Add Integration" and search for "Airkey".
3. Enter your API key and configure the update interval.

### Configuration Options

- **API Key**: Your Airkey API key.
- **Update Interval**: How often, in minutes, Home Assistant should poll the API for updates. Default is 15 minutes.

## Usage

After setup, the integration will create a sensor entity in Home Assistant that provides the current status of your Airkey locks. You can view and use this sensor in your automations and dashboards.

## Developer Information

If you wish to contribute to the development of this integration or if you have any issues, please visit the [GitHub repository](https://github.com/yourusername/airkey).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
