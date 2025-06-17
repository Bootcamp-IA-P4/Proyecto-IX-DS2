// src/components/Navbar.jsx
import React from 'react';
import { NavLink } from 'react-router-dom';
import MedicalServicesIcon from '@mui/icons-material/MedicalServices';

const Navbar = () => {
  const activeStyle = {
    color: '#0A74DA', // Azul Profesional
    borderBottom: '2px solid #0A74DA',
  };

  // El objeto con los nombres ya está completo, ¡eso es perfecto!
  const linkData = { 
    '/': 'Inicio', 
    '/predict': 'Predecir', 
    '/image-analysis': 'Análisis de Imagen', // <--- Ya tenías el nombre aquí
    '/history': 'Historial'
  };

  // Obtenemos las rutas del objeto linkData para asegurarnos de que siempre coincidan
  const paths = Object.keys(linkData);

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-6 flex justify-between items-center h-16">
        <NavLink to="/" className="flex items-center gap-2 text-xl font-bold text-blue-600">
          <MedicalServicesIcon />
          <span>AI Stroke Predictor</span>
        </NavLink>
        <div className="flex gap-8 items-center h-full">
          {/* 
            SOLUCIÓN:
            Añadimos '/image-analysis' al array para que el map() lo renderice.
            O mejor aún, generamos el array a partir de las claves del objeto 'linkData'.
          */}
          {paths.map((path) => (
            <NavLink
              key={path}
              to={path}
              // NavLink requiere 'end' para la ruta raíz para que no coincida con todas las demás.
              end={path === '/'} 
              style={({ isActive }) => (isActive ? activeStyle : undefined)}
              className="text-gray-500 font-medium h-full flex items-center pt-1 hover:text-blue-600 transition-colors"
            >
              {linkData[path]}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;