import React, { useState } from 'react';
import PredictionForm from '../components/PredictionForm';
import ResultCard from '../components/ResultCard'; // Importamos el nuevo componente
import { makePrediction } from '../services/api';

const Prediction = () => {
    const [predictionResult, setPredictionResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handlePredict = async (formData) => {
        setLoading(true);
        setError(null);
        setPredictionResult(null);

        try {
            const response = await makePrediction(formData);
            setPredictionResult(response.data);
        } catch (err) {
            let errorMessage = "Ocurrió un error inesperado.";
            if (err.response?.data?.detail) {
                errorMessage = Array.isArray(err.response.data.detail) 
                    ? err.response.data.detail[0].msg 
                    : err.response.data.detail;
            }
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="container mx-auto p-4 md:p-8">
            <div className="text-center mb-10">
                 <h1 className="text-4xl font-bold text-gray-800">Herramienta de Predicción de ACV</h1>
                 <p className="text-lg text-gray-500 mt-2 max-w-2xl mx-auto">Complete el formulario con los datos del paciente para obtener una estimación de riesgo basada en nuestro modelo de IA.</p>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
                <PredictionForm onSubmit={handlePredict} isLoading={loading} />
                <div className="lg:sticky lg:top-24">
                    <ResultCard result={predictionResult} isLoading={loading} error={error} />
                </div>
            </div>
        </div>
    );
};

export default Prediction;