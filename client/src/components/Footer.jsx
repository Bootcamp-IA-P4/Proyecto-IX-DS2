import React from 'react';

const Footer = () => {
    return (
        <footer className="bg-gray-800 text-white mt-auto p-4 shadow-inner">
            <div className="container mx-auto text-center text-sm">
                <p>© {new Date().getFullYear()} AI Stroke Predictor Project. Todos los derechos reservados.</p>
                <p className="mt-1">Desarrollado con ❤️ por <span className="font-semibold">DS II Group</span></p>
            </div>
        </footer>
    );
};

export default Footer;