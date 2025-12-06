import axios from "axios";

const API_URL = "http://localhost:8000/api/v1/chats";

export const createConversation = (data, token) =>
  axios.post(`${API_URL}/conversation`, data, { headers: { Authorization: `Bearer ${token}` } });

export const addMessage = (data, token) =>
  axios.post(`${API_URL}/message`, data, { headers: { Authorization: `Bearer ${token}` } });

export const getMessages = (conversation_id, token) =>
  axios.get(`${API_URL}/${conversation_id}/messages`, { headers: { Authorization: `Bearer ${token}` } });

export const deleteConversation = (conversation_id, token) =>
  axios.delete(`${API_URL}/${conversation_id}`, { headers: { Authorization: `Bearer ${token}` } });

export const getHistory = (token) =>
  axios.get(`${API_URL}/historylist`, { headers: { Authorization: `Bearer ${token}` } });
