// src/components/Navbar.jsx
import React from 'react';
import { NavLink } from 'react-router-dom';
import MedicalServicesIcon from '@mui/icons-material/MedicalServices'; // Ejemplo de ícono

const Navbar = () => {
  const activeStyle = {
    color: '#0A74DA', // Azul Profesional
    borderBottom: '2px solid #0A74DA',
  };

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-6 flex justify-between items-center h-16">
        <NavLink to="/" className="flex items-center gap-2 text-xl font-bold text-blue-600">
          <MedicalServicesIcon />
          <span>SaludPredict</span>
        </NavLink>
        <div className="flex gap-8 items-center h-full">
          {['/', '/predict', '/history'].map((path) => {
            const names = { '/': 'Inicio', '/predict': 'Predecir', '/history': 'Historial' };
            return (
              <NavLink
                key={path}
                to={path}
                style={({ isActive }) => (isActive ? activeStyle : undefined)}
                className="text-gray-500 font-medium h-full flex items-center pt-1 hover:text-blue-600 transition-colors"
              >
                {names[path]}
              </NavLink>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;