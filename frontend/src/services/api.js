import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL ||
    "https://careerpilot-ai-gq8m.onrender.com/api/v1",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("careerpilot_token");

  if (token) {
    config.headers["X-Auth-Token"] = token;
  }

  return config;
});

export default api;