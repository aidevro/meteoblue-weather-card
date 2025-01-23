# Meteoblue Weather Card

A custom weather card for Home Assistant that displays Meteoblue weather data.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

## Installation

### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz) installed
2. Add this repository as a custom repository in HACS
3. Search for "Meteoblue Weather Card" in the Frontend section
4. Click Install
5. Refresh your browser

### Manual Installation

1. Download `meteoblue-weather-card.js` from the latest release
2. Copy it to your `config/www` directory
3. Add a reference to the card in your `ui-lovelace.yaml`:

```yaml
resources:
  - url: /local/meteoblue-weather-card.js
    type: module
```

## Configuration

Add the card to your dashboard:

```yaml
type: custom:meteoblue-weather-card
entity: weather.meteoblue
name: Weather
show_forecast: true
show_hourly: true
```

### Options

| Name | Type | Default | Description |
|------|------|---------|-------------|
| entity | string | Required | The weather entity ID |
| name | string | Optional | Card title |
| show_forecast | boolean | true | Show daily forecast |
| show_hourly | boolean | true | Show hourly forecast |

## Requirements

- Home Assistant
- Meteoblue integration configured
- HACS (for easy installation)

## Support

If you find this card helpful, consider:
- Adding a star to the repository
- Reporting issues
- Contributing to the code

## License

This project is under the MIT License.