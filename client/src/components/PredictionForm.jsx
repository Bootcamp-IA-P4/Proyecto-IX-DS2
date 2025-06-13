import React, { useState } from 'react';

const PredictionForm = ({ onSubmit, isLoading }) => {
    const [formData, setFormData] = useState({
        gender: 0,
        age: 50,
        hypertension: 0,
        heart_disease: 0,
        ever_married: 1,
        Residence_type: 1,
        avg_glucose_level: 100.0,
        bmi: 25.0,
        work_type: "Private",
        smoking_status: "never smoked",
    });

    const handleChange = (e) => {
        const { name, value, type } = e.target;
        const finalValue = type === 'number' ? parseFloat(value) : value;
        setFormData(prev => ({ ...prev, [name]: finalValue }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData); // Pasamos los datos del formulario al padre
    };

    // Componente interno para campos del formulario para no repetir código
    const FormField = ({ label, name, type = "number", options = [], ...rest }) => (
        <div className="mb-4">
            <label htmlFor={name} className="block text-gray-700 text-sm font-bold mb-2">{label}</label>
            {type === 'select' ? (
                <select name={name} id={name} value={formData[name]} onChange={handleChange} {...rest} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                    {options.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
                </select>
            ) : (
                <input type={type} name={name} id={name} value={formData[name]} onChange={handleChange} {...rest} className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
            )}
        </div>
    );
    
    return (
        <div className="bg-white p-6 rounded-lg shadow-xl">
            <h2 className="text-2xl font-semibold mb-4">Ingrese los datos del paciente</h2>
            <form onSubmit={handleSubmit}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <FormField label="Edad" name="age" />
                    <FormField label="Género" name="gender" type="select" options={[{ value: 1, label: 'Masculino' }, { value: 0, label: 'Femenino' }]} />
                    <FormField label="BMI" name="bmi" step="0.1" />
                    <FormField label="Nivel de Glucosa" name="avg_glucose_level" step="0.1" />
                    <FormField label="Tipo de Trabajo" name="work_type" type="select" options={["Private", "Self-employed", "Govt_job", "children"].map(o => ({ value: o, label: o }))} />
                    <FormField label="Estado de Tabaquismo" name="smoking_status" type="select" options={["never smoked", "formerly smoked", "smokes", "Unknown"].map(o => ({ value: o, label: o }))} />
                    {/* Añade el resto de los selectores binarios aquí si lo deseas (hipertensión, etc.) */}
                </div>
                <button type="submit" disabled={isLoading} className="mt-6 w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:bg-blue-300">
                    {isLoading ? 'Prediciendo...' : 'Obtener Predicción'}
                </button>
            </form>
        </div>
    );
};

export default PredictionForm;