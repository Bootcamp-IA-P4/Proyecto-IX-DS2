import React, { useState } from 'react';
import PredictionForm from '../components/PredictionForm';
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
            
            if (err.response && err.response.data) {
                if (err.response.data.detail && Array.isArray(err.response.data.detail)) {
                    const firstError = err.response.data.detail[0];
                    errorMessage = `${firstError.msg} (campo: ${firstError.loc.join(' -> ')})`;
                } else if (err.response.data.detail) {
                    errorMessage = err.response.data.detail;
                }
            }
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="container mx-auto p-4 md:p-8">
            <div className="text-center mb-8">
                 <h1 className="text-3xl md:text-4xl font-bold text-gray-800">Herramienta de Predicción</h1>
                 <p className="text-gray-500 mt-2">Ingrese los datos para obtener una predicción de riesgo.</p>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
                <PredictionForm onSubmit={handlePredict} isLoading={loading} />
                
                <div className="bg-white rounded-xl shadow-md p-6 flex flex-col items-center justify-center min-h-[300px] lg:sticky lg:top-24">
                    <h2 className="text-2xl font-bold text-gray-800 mb-4">Resultado</h2>
                    {loading && <p className="text-lg text-gray-500">Procesando...</p>}
                    {error && (
                        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 w-full" role="alert">
                            <p className="font-bold">Error de Validación</p>
                            <p>{error}</p> {/* Ahora 'error' es un string seguro para renderizar */}
                        </div>
                    )}
                    {predictionResult && (
                        <div className="text-center">
                            <p className="text-xl text-gray-600 mb-2">Riesgo de Derrame:</p>
                            <p className={`text-4xl font-bold ${predictionResult.stroke === 1 ? 'text-red-600' : 'text-green-600'}`}>
                                {predictionResult.stroke === 1 ? 'Alto Riesgo' : 'Bajo Riesgo'}
                            </p>
                            <p className="text-lg text-gray-500 mt-4">
                                Probabilidad: <span className="font-bold text-gray-800">{predictionResult.probability}</span>
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Prediction;