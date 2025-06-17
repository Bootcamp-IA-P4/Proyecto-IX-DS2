import axios from 'axios';

const baseURL = import.meta.env.DEV 
  ? import.meta.env.VITE_API_BASE_URL
  : import.meta.env.VITE_API_BASE_URL_DOCKER;

console.log(`API baseURL set to: ${baseURL}`);

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const makePrediction = (formData) => {
  return apiClient.post('/predict', formData);
};

export const getHistory = () => {
  return apiClient.get('/all-predicts');
};

export const predictWithImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile); 

  try {
    const response = await apiClient.post(
      '/predict-image',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    
    return response.data;

  } catch (error) {
    console.error("Error en la llamada a predictWithImage:", error.response?.data || error.message);
    throw error.response?.data || new Error("Error de red o del servidor");
  }
};