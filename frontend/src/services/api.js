import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const askQuestion = async (question) => {
  const response = await axios.post(`${API_URL}/ask`, { question });
  return response.data;
};

export const submitFeedback = async (feedbackData) => {
  const response = await axios.post(`${API_URL}/feedback`, feedbackData);
  return response.data;
};