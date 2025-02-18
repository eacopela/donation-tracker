const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');
const express = require('express');

module.exports = function(app) {
  // Serve the data directory
  app.use('/data', express.static(path.join(__dirname, '../data')));
};
