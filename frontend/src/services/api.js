import axios from 'axios';

const BASE_URL = "http://localhost:8000";

export const analyzeSyntax = async (text) => {
  const response = await axios.post(`${BASE_URL}/analyze/syntax`, { text });
  return response.data;
};

export const analyzeNER = async (text) => {
  const response = await axios.post(`${BASE_URL}/analyze/ner`, { text });
  return response.data;
};

export const analyzeTopics = async (text) => {
  const response = await axios.post(`${BASE_URL}/analyze/topics`, { text });
  return response.data;
};

export const analyzePOS = async (text) => {
  const response = await axios.post(`${BASE_URL}/analyze/pos`, { text });
  return response.data;
};

export const getStatistics = async () => {
  const response = await axios.get(`${BASE_URL}/statistics`);
  return response.data;
};

export const getPOSStatistics = async () => {
  const response = await axios.get(`${BASE_URL}/analyze/pos/statistics`);
  return response.data;
};

export const getNERStatistics = async () => {
  const response = await axios.get(`${BASE_URL}/analyze/ner/statistics`);
  return response.data;
};

export const getLanguageStatistics = async () => {
  const response = await axios.get(`${BASE_URL}/analyze/language/statistics`);
  return response.data;
};

export const getBigramProbability = async (text) => {
  const response = await axios.post(`${BASE_URL}/analyze/language/bigram-probability`, { text });
  return response.data;
};