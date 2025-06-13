import React, { useState } from 'react';
import PersonIcon from '@mui/icons-material/Person';
import MonitorHeartIcon from '@mui/icons-material/MonitorHeart';
import WorkIcon from '@mui/icons-material/Work';

// Componente para una sección del formulario
const FormSection = ({ title, icon, children }) => (
    <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
            {icon}
            <h3 className="text-xl font-bold text-gray-700">{title}</h3>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
            {children}
        </div>
    </div>
);

// Componente para un campo del formulario (Input/Select)
const FormField = ({ label, name, type = "number", options = [], value, onChange, ...rest }) => (
    <div>
        <label htmlFor={name} className="block text-sm font-medium text-gray-600 mb-1">{label}</label>
        {type === 'select' ? (
            <select
                name={name}
                id={name}
                value={value}
                onChange={onChange}
                className="w-full p-2.5 bg-white border border-gray-300 text-gray-900 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 transition"
                {...rest}
            >
                {options.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
            </select>
        ) : (
            <input
                type={type}
                name={name}
                id={name}
                value={value}
                onChange={onChange}
                className="w-full p-2.5 bg-white border border-gray-300 text-gray-900 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 transition"
                {...rest}
            />
        )}
    </div>
);


const PredictionForm = ({ onSubmit, isLoading }) => {
    const [formData, setFormData] = useState({
        gender: 1, age: 50, hypertension: 0, heart_disease: 0,
        ever_married: 1, Residence_type: 1, avg_glucose_level: 100.0,
        height: 170, weight: 70, work_type: "Private", smoking_status: "never smoked",
    });

    const handleChange = (e) => {
        const { name, value, type } = e.target;
        
        // --- SOLUCIÓN AL BUG ---
        // Para inputs numéricos, solo parseamos a número si no está vacío.
        // Mantenemos el string mientras el usuario escribe para evitar el re-render.
        const parsedValue = (type === 'number' && value !== '') ? parseFloat(value) : value;

        setFormData(prev => ({
            ...prev,
            [name]: parsedValue
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Aseguramos que todos los valores numéricos se envíen como números.
        const numericData = {
            ...formData,
            gender: Number(formData.gender),
            age: Number(formData.age),
            hypertension: Number(formData.hypertension),
            heart_disease: Number(formData.heart_disease),
            ever_married: Number(formData.ever_married),
            Residence_type: Number(formData.Residence_type),
        };
        onSubmit(numericData);
    };

    return (
        <div className="bg-white rounded-xl shadow-lg p-6 md:p-8">
            <form onSubmit={handleSubmit}>
                <FormSection title="Información Demográfica" icon={<PersonIcon className="text-blue-600" />}>
                    <FormField label="Edad" name="age" value={formData.age} onChange={handleChange} />
                    <FormField label="Género" name="gender" type="select" value={formData.gender} onChange={handleChange} options={[{ value: 1, label: 'Masculino' }, { value: 0, label: 'Femenino' }]} />
                    <FormField label="Altura (cm)" name="height" value={formData.height} onChange={handleChange} />
                    <FormField label="Peso (kg)" name="weight" value={formData.weight} onChange={handleChange} />
                </FormSection>
                
                <FormSection title="Historial y Factores de Riesgo" icon={<MonitorHeartIcon className="text-red-500" />}>
                    <FormField label="Hipertensión" name="hypertension" type="select" value={formData.hypertension} onChange={handleChange} options={[{ value: 1, label: 'Sí' }, { value: 0, label: 'No' }]} />
                    <FormField label="Enfermedad Cardíaca" name="heart_disease" type="select" value={formData.heart_disease} onChange={handleChange} options={[{ value: 1, label: 'Sí' }, { value: 0, label: 'No' }]} />
                    <FormField label="Nivel de Glucosa" name="avg_glucose_level" step="0.1" value={formData.avg_glucose_level} onChange={handleChange} />
                    <FormField label="Estado de Tabaquismo" name="smoking_status" type="select" value={formData.smoking_status} onChange={handleChange} options={["never smoked", "formerly smoked", "smokes", "Unknown"].map(o => ({ value: o, label: o }))} />
                </FormSection>

                <FormSection title="Estilo de Vida" icon={<WorkIcon className="text-teal-500" />}>
                    <FormField label="¿Alguna vez se ha casado?" name="ever_married" type="select" value={formData.ever_married} onChange={handleChange} options={[{ value: 1, label: 'Sí' }, { value: 0, label: 'No' }]} />
                    <FormField label="Tipo de Residencia" name="Residence_type" type="select" value={formData.Residence_type} onChange={handleChange} options={[{ value: 1, label: 'Urbana' }, { value: 0, label: 'Rural' }]} />
                    <FormField label="Tipo de Trabajo" name="work_type" type="select" value={formData.work_type} onChange={handleChange} options={["Private", "Self-employed", "Govt_job", "children"].map(o => ({ value: o, label: o }))} />
                </FormSection>

                <button type="submit" disabled={isLoading} className="btn-primary w-full text-lg py-3">
                    {isLoading ? 'Analizando...' : 'Calcular Riesgo'}
                </button>
            </form>
        </div>
    );
};

export default PredictionForm;