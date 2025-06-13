import axios from 'axios';

// Creamos una instancia de axios con la configuración base
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Función para realizar una predicción
export const makePrediction = (formData) => {
  return apiClient.post('/predict', formData);
};

// Función para obtener el historial de predicciones
export const getHistory = () => {
  return apiClient.get('/all-predicts');
};