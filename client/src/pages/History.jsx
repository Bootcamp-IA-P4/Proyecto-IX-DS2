import React, { useState, useEffect } from 'react';
import { getHistory } from '../services/api';

const History = () => {
  // Estados para manejar los datos, la carga, los errores y la fila expandida
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedRow, setExpandedRow] = useState(null);

  // Efecto para obtener el historial cuando el componente se monta
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        const response = await getHistory();
        setPredictions(Array.isArray(response.data) ? response.data : []);
      } catch (err) {
        setError(err.response?.data?.detail || 'No se pudo cargar el historial.');
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  // Función para abrir/cerrar los detalles de una fila
  const toggleRow = (id) => {
    setExpandedRow(expandedRow === id ? null : id);
  };

  // Renderizado mientras se cargan los datos
  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-lg text-gray-500">Cargando historial...</div>
      </div>
    );
  }

  // Renderizado si ocurre un error
  if (error) {
    return (
      <div className="container mx-auto p-8">
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md" role="alert">
          <p className="font-bold">Error</p>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  // Renderizado principal con la tabla de resultados
  return (
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold text-gray-800">Historial de Predicciones</h1>
        <p className="text-lg text-gray-500 mt-2">
          Revisa las últimas predicciones realizadas. Haz clic en una fila para ver los detalles.
        </p>
      </div>
      <div className="overflow-x-auto shadow-lg rounded-xl">
        <table className="min-w-full">
          <thead className="bg-gray-100">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Fecha</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Edad</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Resultado</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">Probabilidad</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {predictions.length === 0 ? (
              <tr>
                <td colSpan="4" className="p-6 text-center text-gray-500">
                  No hay predicciones guardadas todavía.
                </td>
              </tr>
            ) : (
              predictions.map(p => {
                // Creamos un objeto de detalles para la vista expandida, excluyendo las columnas que no nos interesan.
                const { id, created_at, ...details } = p;

                return (
                  <React.Fragment key={p.id}>
                    {/* Fila principal de la tabla */}
                    <tr className="hover:bg-blue-50 cursor-pointer transition-colors duration-200" onClick={() => toggleRow(p.id)}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{new Date(p.created_at).toLocaleString()}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-800">
                        {/* Se lee directamente desde p.age */}
                        {p.age ?? 'N/A'} años
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-bold">
                        <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${p.stroke === 1 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                          {p.stroke === 1 ? 'Alto Riesgo' : 'Bajo Riesgo'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">
                        {/* Se lee directamente desde p.probability */}
                        {p.probability != null ? `${(p.probability * 100).toFixed(1)}%` : 'N/A'}
                      </td>
                    </tr>
                    
                    {/* Fila de detalles expandibles */}
                    {expandedRow === p.id && (
                      <tr className="bg-gray-50">
                        <td colSpan="4" className="px-6 py-4">
                          <h4 className="font-bold text-gray-700 mb-2">Detalles Completos de la Entrada:</h4>
                          <pre className="bg-gray-200 text-gray-800 p-4 rounded-md text-xs whitespace-pre-wrap shadow-inner">
                            {JSON.stringify(details, null, 2)}
                          </pre>
                        </td>
                      </tr>
                    )}
                    </React.Fragment>
                  );
                })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default History;