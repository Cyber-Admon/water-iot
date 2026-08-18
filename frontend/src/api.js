import axios from "axios";

// Change this if your backend runs somewhere other than localhost:8000
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: {
    "ngrok-skip-browser-warning": "true",
  },
});

// Each function here maps to one backend endpoint.
// Keeping them in one file means if the API URL structure ever changes,
// you only update it here, not scattered across every component.

export const getLatestReadings = async () => {
  const response = await api.get("/api/readings/latest");
  return response.data;
};

export const getReadingsHistory = async (nodeId, limit = 50) => {
  const response = await api.get("/api/readings", {
    params: { node_id: nodeId, limit },
  });
  return response.data;
};

export const getAlerts = async (limit = 20) => {
  const response = await api.get("/api/alerts", { params: { limit } });
  return response.data;
};

export const getNodes = async () => {
  const response = await api.get("/api/nodes");
  return response.data;
};

export default api;
