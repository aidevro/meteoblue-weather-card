import { html, css, LitElement } from 'lit';
import { property } from 'lit/decorators.js';

class MeteoblueWeatherCard extends LitElement {
  @property({ type: Object }) hass;
  @property({ type: Object }) config;

  static get properties() {
    return {
      hass: { type: Object },
      config: { type: Object },
    };
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('Please define an entity');
    }
    this.config = config;
  }

  shouldUpdate(changedProps) {
    if (changedProps.has('config') || changedProps.has('hass')) {
      return true;
    }
    
    const oldHass = changedProps.get('hass');
    if (oldHass) {
      return oldHass.states[this.config.entity] !== this.hass.states[this.config.entity];
    }
    return false;
  }

  render() {
    if (!this.config || !this.hass) {
      return html``;
    }

    const stateObj = this.hass.states[this.config.entity];
    
    if (!stateObj) {
      return html`
        <hui-warning>
          Entity not available: ${this.config.entity}
        </hui-warning>
      `;
    }

    return html`
      <ha-card>
        <div class="card-content">
          <div class="header">
            <div class="name">
              ${this.config.name || stateObj.attributes.friendly_name}
            </div>
            <div class="temp">
              ${stateObj.attributes.temperature}°C
            </div>
          </div>
          
          <div class="current-container">
            <div class="current">
              <div class="condition">
                <ha-icon icon="mdi:${this._getWeatherIcon(stateObj.state)}"></ha-icon>
                <span>${stateObj.state}</span>
              </div>
              <div class="details">
                <div>
                  <ha-icon icon="mdi:water-percent"></ha-icon>
                  ${stateObj.attributes.humidity}%
                </div>
                <div>
                  <ha-icon icon="mdi:weather-windy"></ha-icon>
                  ${stateObj.attributes.wind_speed} km/h
                </div>
                <div>
                  <ha-icon icon="mdi:gauge"></ha-icon>
                  ${stateObj.attributes.pressure} hPa
                </div>
              </div>
            </div>
          </div>
          
          ${this._renderForecast(stateObj)}
        </div>
      </ha-card>
    `;
  }

  _renderForecast(stateObj) {
    if (!this.config.show_forecast || !stateObj.attributes.forecast) {
      return html``;
    }

    return html`
      <div class="forecast">
        ${stateObj.attributes.forecast.slice(0, 5).map(
          daily => html`
            <div class="day">
              <div class="date">
                ${new Date(daily.datetime).toLocaleDateString(undefined, { weekday: 'short' })}
              </div>
              <ha-icon icon="mdi:${this._getWeatherIcon(daily.condition)}"></ha-icon>
              <div class="temp-container">
                <div class="temp-high">
                  ${daily.temperature}°
                </div>
                ${daily.templow !== undefined ? html`
                  <div class="temp-low">
                    ${daily.templow}°
                  </div>
                ` : ''}
              </div>
              <div class="precipitation">
                ${daily.precipitation !== undefined ? html`
                  <ha-icon icon="mdi:water"></ha-icon>
                  ${daily.precipitation} mm
                ` : ''}
              </div>
            </div>
          `
        )}
      </div>
    `;
  }

  _getWeatherIcon(condition) {
    const icons = {
      'clear-night': 'weather-night',
      'cloudy': 'weather-cloudy',
      'exceptional': 'alert-circle-outline',
      'fog': 'weather-fog',
      'hail': 'weather-hail',
      'lightning': 'weather-lightning',
      'lightning-rainy': 'weather-lightning-rainy',
      'partlycloudy': 'weather-partly-cloudy',
      'pouring': 'weather-pouring',
      'rainy': 'weather-rainy',
      'snowy': 'weather-snowy',
      'snowy-rainy': 'weather-snowy-rainy',
      'sunny': 'weather-sunny',
      'windy': 'weather-windy',
      'windy-variant': 'weather-windy-variant'
    };
    return icons[condition] || 'help-circle-outline';
  }

  static get styles() {
    return css`
      ha-card {
        --ha-card-background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        padding: 16px;
      }
      
      .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
      }
      
      .name {
        font-size: 1.5em;
        font-weight: 500;
      }
      
      .temp {
        font-size: 2em;
        font-weight: bold;
      }
      
      .current-container {
        margin-bottom: 24px;
      }
      
      .current {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      
      .condition {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1.2em;
      }
      
      .details {
        display: flex;
        justify-content: space-between;
        gap: 16px;
      }
      
      .details div {
        display: flex;
        align-items: center;
        gap: 4px;
      }
      
      .forecast {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 16px;
      }
      
      .day {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 8px;
      }
      
      .date {
        font-weight: 500;
      }
      
      .temp-container {
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      
      .temp-high {
        font-weight: 500;
      }
      
      .temp-low {
        color: var(--secondary-text-color);
        font-size: 0.9em;
      }
      
      .precipitation {
        display: flex;
        align-items: center;
        gap: 4px;
        color: var(--secondary-text-color);
        font-size: 0.9em;
      }
    `;
  }
}

customElements.define('meteoblue-weather-card', MeteoblueWeatherCard);
