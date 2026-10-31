import axios from "axios";

const tokenKey = "smart-travel-access-token";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(tokenKey);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export function saveAccessToken(token: string) {
  localStorage.setItem(tokenKey, token);
}

export function clearAccessToken() {
  localStorage.removeItem(tokenKey);
}

export function hasAccessToken() {
  return localStorage.getItem(tokenKey) !== null;
}

export default api;
