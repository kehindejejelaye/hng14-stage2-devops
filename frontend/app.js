const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

// Configuration from environment variables
const PORT = process.env.PORT || 3000;
const API_HOST = process.env.API_HOST || "localhost";
const API_PORT = process.env.API_PORT || 8000;
const API_URL = `http://${API_HOST}:${API_PORT}`;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`);
    res.json(response.data);
  } catch (err) {
    console.error(`Error submitting job to ${API_URL}:`, err.message);
    res.status(500).json({ error: "something went wrong" });
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    console.error(`Error fetching job ${req.params.id} status:`, err.message);
    res.status(500).json({ error: "something went wrong" });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Frontend running on port ${PORT}`);
  console.log(`Communicating with API at ${API_HOST}:${API_PORT}`);
});
