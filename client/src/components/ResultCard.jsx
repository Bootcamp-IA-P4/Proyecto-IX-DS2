import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Label } from 'recharts';

const ResultCard = ({ result, isLoading, error }) => {
    
    const probability = result ? parseFloat(result.probability.replace(' %', '')) : 0;
    const isHighRisk = result?.stroke === 1;

    const data = [
        { name: 'Riesgo', value: probability },
        { name: 'Seguridad', value: 100 - probability }
    ];

    const COLORS = [isHighRisk ? '#EF4444' : '#10B981', '#E5E7EB'];

    const renderContent = () => {
        if (isLoading) {
            return <p className="text-lg text-gray-500">Analizando datos...</p>;
        }
        if (error) {
            return (
                <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 w-full rounded-r-md" role="alert">
                    <p className="font-bold">Error de Validación</p>
                    <p>{error}</p>
                </div>
            );
        }
        if (result) {
            return (
                <div className="w-full text-center">
                    <div className="h-60 w-full">
                        <ResponsiveContainer>
                            <PieChart>
                                <Pie data={data} cx="50%" cy="50%" innerRadius={70} outerRadius={90} startAngle={180} endAngle={-180} fill="#8884d8" paddingAngle={0} dataKey="value">
                                    {data.map((entry, index) => ( <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="none"/> ))}
                                    <Label 
                                        value={`${probability.toFixed(1)}%`}
                                        position="center" 
                                        className="text-4xl font-bold fill-gray-800"
                                    />
                                </Pie>
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                    <p className={`text-2xl font-bold mt-4 ${isHighRisk ? 'text-red-600' : 'text-green-600'}`}>
                        {isHighRisk ? 'Riesgo Alto Detectado' : 'Riesgo Bajo'}
                    </p>
                    <p className="text-gray-500 mt-1">Probabilidad de ACV estimada</p>
                    <div className="mt-6 p-4 bg-gray-100 rounded-lg text-sm text-left">
                        <p className="font-semibold text-gray-700">Recordatorio:</p>
                        <p className="text-gray-600">Este resultado es una estimación basada en un modelo y no reemplaza el diagnóstico de un profesional médico. Consulte a su doctor.</p>
                    </div>
                </div>
            );
        }
        return <p className="text-gray-500">El resultado de la predicción aparecerá aquí.</p>;
    };

    return (
        <div className="bg-white rounded-xl shadow-lg p-6 flex flex-col items-center justify-center min-h-[400px]">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 self-start">Resultado del Análisis</h2>
            {renderContent()}
        </div>
    );
};

export default ResultCard;