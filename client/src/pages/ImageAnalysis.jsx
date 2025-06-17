import React from 'react';
import ImagePredictionForm from '../components/ImagePredictionForm';

const ImageAnalysis = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-gray-800 tracking-tight lg:text-5xl">
          Análisis de Brain Stroke por Imagen
        </h1>
        <p className="mt-4 max-w-2xl mx-auto text-xl text-gray-600">
          Sube una imagen de resonancia magnética o tomografía computarizada para que nuestro modelo de IA la analice.
        </p>
      </div>
      
      <ImagePredictionForm />
    </div>
  );
};

export default ImageAnalysis;