import React, { useState, useEffect } from 'react';
import { getHistory } from '../services/api'; // Importamos desde el servicio

const History = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        const response = await getHistory(); // Usamos la función del servicio
        setPredictions(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'No se pudo cargar el historial.');
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  if (loading) return <div className="text-center p-8">Cargando historial...</div>;
  if (error) return <div className="text-center p-8 text-red-500">Error: {error}</div>;

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Historial de Predicciones</h1>
      <div className="overflow-x-auto bg-white rounded-lg shadow">
        <table className="min-w-full">
          <thead className="bg-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Fecha</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Input</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Predicción (Stroke)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {predictions.length === 0 ? (
              <tr><td colSpan="3" className="p-4 text-center text-gray-500">No hay predicciones guardadas.</td></tr>
            ) : (
              predictions.map(p => (
                <tr key={p.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-800">{new Date(p.created_at).toLocaleString()}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    <pre className="bg-gray-100 p-2 rounded text-xs">{JSON.stringify(p.input, null, 2)}</pre>
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm font-bold ${p.stroke === 1 ? 'text-red-600' : 'text-green-600'}`}>
                    {p.stroke === 1 ? 'Sí' : 'No'}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default History;