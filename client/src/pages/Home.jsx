import React from 'react';
import { NavLink } from 'react-router-dom';

const Home = () => {
    return (
        <div className="container mx-auto px-6 py-12 md:py-20">
            {/* Sección de Hero */}
            <div className="text-center">
                <span className="text-blue-600 font-semibold">Plataforma de IA para la Salud</span>
                <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mt-2 mb-4 leading-tight">
                    Predecir el Riesgo de ACV con Confianza
                </h1>
                <p className="text-lg text-gray-500 max-w-2xl mx-auto mb-8">
                    Utilice nuestro modelo de machine learning de última generación para evaluar el riesgo de accidente cerebrovascular basado en datos clave del paciente. Una herramienta de apoyo para profesionales de la salud.
                </p>
                <NavLink to="/predict" className="btn-primary px-8 py-3 text-lg">
                    Iniciar Predicción
                </NavLink>
            </div>

            {/* Sección de Características */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20 text-center">
                <FeatureCard 
                    title="Análisis Instantáneo"
                    description="Reciba resultados en segundos. Nuestro modelo procesa los datos en tiempo real para una evaluación rápida."
                />
                <FeatureCard 
                    title="Basado en Evidencia"
                    description="Entrenado con miles de registros anonimizados para garantizar una alta precisión y fiabilidad en las predicciones."
                />
                <FeatureCard 
                    title="Seguro y Confiable"
                    description="La privacidad de los datos es nuestra prioridad. Toda la información es manejada de forma segura y confidencial."
                />
            </div>
        </div>
    );
};

// Pequeño componente para las tarjetas de características
const FeatureCard = ({ title, description }) => (
    <div className="bg-white rounded-xl shadow-md p-8 hover:shadow-lg transition-shadow">
        <h3 className="text-xl font-bold text-gray-800 mb-2">{title}</h3>
        <p className="text-gray-500">{description}</p>
    </div>
);


export default Home;