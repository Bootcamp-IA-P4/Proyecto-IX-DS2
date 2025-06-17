import React, { useState } from 'react';
import { predictWithImage } from '../services/api'; // Importamos la función específica

const ImagePredictionForm = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && (file.type === "image/jpeg" || file.type === "image/png")) {
      setSelectedFile(file);
      const objectUrl = URL.createObjectURL(file);
      setPreview(objectUrl);
      setResult(null); 
      setError('');
    } else {
      setSelectedFile(null);
      setPreview(null);
      setError('Por favor, selecciona un archivo de imagen válido (JPG o PNG).');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError('No se ha seleccionado ninguna imagen.');
      return;
    }

    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      // Pasamos directamente el objeto File a nuestra función de servicio.
      const response = await predictWithImage(selectedFile);
      setResult(response);
    } catch (err) {
      setError(err.detail || 'Hubo un error al procesar la imagen. Inténtalo de nuevo.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Función para obtener texto y estilo basados en la predicción
  const getPredictionDetails = (prediction) => {
    if (prediction === 1) {
      return {
        text: 'Brain Stroke Detectado',
        className: 'bg-red-100 text-red-800',
      };
    }
    return {
      text: 'Normal',
      className: 'bg-green-100 text-green-800',
    };
  };

  return (
    <div className="w-full max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-lg">
      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <label htmlFor="image-upload" className="block text-gray-700 text-lg font-bold mb-2">
            Sube una imagen del escáner cerebral
          </label>
          <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
            <div className="space-y-1 text-center">
              {preview ? (
                <img src={preview} alt="Vista previa" className="mx-auto h-48 w-auto rounded-lg" />
              ) : (
                <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              )}
              <div className="flex text-sm text-gray-600">
                <label htmlFor="image-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none">
                  <span>Carga un archivo</span>
                  <input id="image-upload" name="image-upload" type="file" className="sr-only" accept="image/png, image/jpeg" onChange={handleFileChange} />
                </label>
                <p className="pl-1">o arrástralo aquí</p>
              </div>
              <p className="text-xs text-gray-500">JPG, PNG</p>
            </div>
          </div>
        </div>
        
        <div className="flex items-center justify-center">
          <button
            type="submit"
            disabled={!selectedFile || isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg focus:outline-none focus:shadow-outline transition duration-300 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Analizando...' : 'Obtener Predicción'}
          </button>
        </div>
      </form>

      {error && <p className="mt-4 text-center text-red-500 font-semibold">{error}</p>}
      
      {result && (
        <div className="mt-8 p-6 bg-gray-50 rounded-lg border">
          <h3 className="text-xl font-bold text-gray-900 mb-2 text-center">Resultado del Análisis</h3>
          <div className={`text-center p-4 rounded-md ${getPredictionDetails(result.prediction).className}`}>
             <p className="text-2xl font-bold">{getPredictionDetails(result.prediction).text}</p>
             <p className="text-lg">Probabilidad: {(result.probability * 100).toFixed(2)}%</p>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">Archivo guardado como: {result.filename}</p>
        </div>
      )}
    </div>
  );
};

export default ImagePredictionForm;