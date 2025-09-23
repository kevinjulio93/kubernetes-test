const express = require('express');
const path = require('path');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:5000';

// Servir ruta de configuración para que el frontend pueda leer la URL
app.get('/config', (req, res) => {
  res.json({ API_BASE });
});

// Servir archivos estáticos desde la carpeta actual
app.use(express.static(path.join(__dirname)));

const port = process.env.PORT || 8000;
app.listen(port, () => {
  console.log(`Frontend server listening on http://127.0.0.1:${port}`);
});
