# Zone4 Remote for Home Assistant

A custom component that allows for control of the APART Zone4 pre-amp over serial.

## HACS Installation

1. Open HACS in Home Assistant.
2. Click on "Integrations".
3. Click on the three dots in the top right corner.
4. Click on "Custom repositories".
5. Add the following repository URL: https://github.com/samjsmart/ha-zone4
6. Select "Integration" as the category.
7. Click on "Add".
8. Install the "Zone4 Remote" integration from the HACS store.

## Manual Installation

1. Download the latest release from the [releases page](https://github.com/samjsmart/ha-zone4/releases).
2. Extract the downloaded ZIP file.
3. Copy the `zone4` directory to your Home Assistant `custom_components` directory.
4. Restart Home Assistant.
5. Configure the integration as described below.

## Configuration

Add the following to your `configuration.yaml` file:

```yaml
media_player:
  - platform: zone4
    port: /dev/ttyUSB0
    zone_names: # Optional
      "1": "Garden"
      "2": "Kitchen"
      "3": "Living Room"
      "4": "Office"
```

## Notes

We recommend using the [@kaljih Mini Media Player custom card](https://github.com/kalkih/mini-media-player) to display the current state of your APART Zone4 pre-amp in Home Assistant.

## Credits

This integration was created by [Sam Smart](https://github.com/samjsmart).

## License

This integration is licensed under the [MIT License](LICENSE.md).
