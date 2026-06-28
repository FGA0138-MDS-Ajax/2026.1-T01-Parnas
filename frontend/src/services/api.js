import axios from "axios";

export const getStoredToken = () => {
  const directToken = localStorage.getItem("token");
  if (directToken) return directToken;

  const fallbackToken = localStorage.getItem("access_token");
  if (fallbackToken) return fallbackToken;

  return null;
};

const api = axios.create({
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token = getStoredToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export default api;
