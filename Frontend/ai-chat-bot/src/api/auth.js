import axios from "axios";

const API_URL = "http://localhost:8000/api/v1/users";

export const registerUser = (data) => axios.post(`${API_URL}/register`, data);

export const loginUser = (data) => axios.post(`${API_URL}/login`, data);

export const logoutUser = (token) => axios.post(
  `${API_URL}/logout`,
  {},
  { headers: { Authorization: `Bearer ${token}` } }
);

export const getUserDetails = (token) => axios.get(
  `${API_URL}/me`,
  { headers: { Authorization: `Bearer ${token}` } }
);
