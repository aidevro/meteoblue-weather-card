const path = require('path');

module.exports = {
  entry: './src/meteoblue-weather-card.js',
  output: {
    filename: 'meteoblue-weather-card.js',
    path: path.resolve(__dirname, 'dist'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
            plugins: [
              ['@babel/plugin-proposal-decorators', { legacy: true }]
            ]
          }
        }
      }
    ]
  },
  mode: 'production'
};
