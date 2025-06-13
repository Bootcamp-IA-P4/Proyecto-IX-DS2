import React, { useState } from 'react';
import PredictionForm from '../components/PredictionForm';
import { makePrediction } from '../services/api'; // Importamos la función del servicio

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
            setError(err.response?.data?.detail || 'Ocurrió un error inesperado.');
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div className="container mx-auto p-8">
            <h1 className="text-4xl font-bold text-center mb-8">Predicción de Derrame Cerebral</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
                {/* Columna del Formulario */}
                <PredictionForm onSubmit={handlePredict} isLoading={loading} />
                
                {/* Columna de Resultados */}
                <div className="bg-gray-50 p-6 rounded-lg shadow-xl flex flex-col items-center justify-center min-h-[300px]">
                    <h2 className="text-2xl font-semibold mb-4">Resultado</h2>
                    {loading && <p className="text-lg">Procesando...</p>}
                    {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded"><strong className="font-bold">Error:</strong> {error}</div>}
                    {predictionResult && (
                        <div className="text-center">
                            <p className="text-xl mb-2">
                                ¿Riesgo de Derrame?: <span className={`font-bold ${predictionResult.stroke === 1 ? 'text-red-600' : 'text-green-600'}`}>{predictionResult.stroke === 1 ? 'Sí' : 'No'}</span>
                            </p>
                            <p className="text-lg">
                                Probabilidad: <span className="font-bold">{predictionResult.probability}</span>
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Prediction;