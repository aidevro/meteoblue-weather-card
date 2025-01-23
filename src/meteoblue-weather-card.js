import { html, css, LitElement } from 'lit';
import { property } from 'lit/decorators.js';

class MeteoblueWeatherCard extends HTMLElement {
  set hass(hass) {
    if (!this.content) {
      this.innerHTML = `
        <ha-card>
          <div class="card-content">
            <div class="current">
              <div class="temp"></div>
              <div class="details">
                <div class="humidity"></div>
                <div class="pressure"></div>
                <div class="wind"></div>
              </div>
            </div>
            <div class="forecast"></div>
          </div>
        </ha-card>
      `;
      this.content = true;
    }

    const entityId = this.config.entity;
    const state = hass.states[entityId];
    
    if (state) {
      const current = state.attributes;
      
      this.querySelector('.temp').textContent = 
        `${state.attributes.temperature}°C`;
      
      this.querySelector('.humidity').textContent = 
        `Humidity: ${state.attributes.humidity}%`;
      
      this.querySelector('.pressure').textContent = 
        `Pressure: ${state.attributes.pressure} hPa`;
      
      this.querySelector('.wind').textContent = 
        `Wind: ${state.attributes.wind_speed} m/s`;

      const forecast = state.attributes.forecast;
      if (forecast) {
        const forecastEl = this.querySelector('.forecast');
        forecastEl.innerHTML = forecast.map(daily => `
          <div class="day">
            <div>${new Date(daily.datetime).toLocaleDateString()}</div>
            <div>${daily.temperature}°C</div>
            <div>${daily.templow}°C</div>
            <div>${daily.precipitation}mm</div>
          </div>
        `).join('');
      }
    }
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('Please define an entity');
    }
    this.config = config;
  }

  getCardSize() {
    return 3;
  }

  static getStubConfig() {
    return {
      entity: "weather.meteoblue",
    };
  }
}

customElements.define('meteoblue-weather-card', MeteoblueWeatherCard);
