import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth.jsx';
import { NoteIcon, CheckIcon, ArchiveIcon } from './icons';
import './NoteForm.css';

const NoteForm = ({ note, onSubmit, onCancel, title }) => {
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    status: 'draft',
    tags: []
  });
  const [tagInput, setTagInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  // Cargar datos de la nota si estamos editando
  useEffect(() => {
    if (note) {
      // Mapear estados del backend al frontend para edición
      const backendToFrontendStatus = {
        'draft': 'draft',
        'published': 'published',  // Mantener published como published
        'archived': 'archived'
      };
      
      setFormData({
        title: note.title || '',
        content: note.content || '',
        status: backendToFrontendStatus[note.status] || 'draft',
        tags: note.tags || []
      });
    }
  }, [note]);

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.title.trim()) {
      newErrors.title = 'El título es obligatorio';
    } else if (formData.title.length > 200) {
      newErrors.title = 'El título no puede exceder 200 caracteres';
    }
    
    if (!formData.content.trim()) {
      newErrors.content = 'El contenido es obligatorio';
    } else if (formData.content.length > 10000) {
      newErrors.content = 'El contenido no puede exceder 10,000 caracteres';
    }
    
    if (formData.tags.length > 10) {
      newErrors.tags = 'No puedes agregar más de 10 etiquetas';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Limpiar error del campo cuando el usuario empiece a escribir
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleAddTag = (e) => {
    e.preventDefault();
    const tag = tagInput.trim().toLowerCase();
    
    if (tag && !formData.tags.includes(tag) && formData.tags.length < 10) {
      setFormData(prev => ({
        ...prev,
        tags: [...prev.tags, tag]
      }));
      setTagInput('');
      
      // Limpiar error de tags si existe
      if (errors.tags) {
        setErrors(prev => ({
          ...prev,
          tags: ''
        }));
      }
    }
  };

  const handleRemoveTag = (tagToRemove) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToRemove)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    
    try {
      await onSubmit(formData);
    } catch (error) {
      console.error('Error submitting form:', error);
      // El error se maneja en el componente padre
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.target.name === 'tagInput') {
      handleAddTag(e);
    }
  };

  return (
    <div className="note-form-container">
      <div className="note-form-header">
        <h2 className="note-form-title">{title || 'Nota'}</h2>
        <button 
          className="close-btn"
          onClick={onCancel}
          type="button"
          disabled={loading}
        >
          ✕
        </button>
      </div>
      
      <form onSubmit={handleSubmit} className="note-form">
        {/* Título */}
        <div className="form-group">
          <label htmlFor="title" className="form-label">
            Título *
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleInputChange}
            className={`form-input ${errors.title ? 'error' : ''}`}
            placeholder="Escribe el título de tu nota..."
            maxLength={200}
            disabled={loading}
          />
          {errors.title && (
            <span className="error-message">{errors.title}</span>
          )}
          <div className="char-counter">
            {formData.title.length}/200
          </div>
        </div>

        {/* Estado */}
        <div className="form-group">
          <label htmlFor="status" className="form-label">
            Estado
          </label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleInputChange}
            className="form-select"
            disabled={loading}
          >
            <option value="draft"><NoteIcon size={16} /> Borrador</option>
            <option value="published"><CheckIcon size={16} /> Publicada</option>
            <option value="archived"><ArchiveIcon size={16} /> Archivada</option>
          </select>
        </div>

        {/* Contenido */}
        <div className="form-group">
          <label htmlFor="content" className="form-label">
            Contenido *
          </label>
          <textarea
            id="content"
            name="content"
            value={formData.content}
            onChange={handleInputChange}
            className={`form-textarea ${errors.content ? 'error' : ''}`}
            placeholder="Escribe el contenido de tu nota..."
            rows={8}
            maxLength={10000}
            disabled={loading}
          />
          {errors.content && (
            <span className="error-message">{errors.content}</span>
          )}
          <div className="char-counter">
            {formData.content.length}/10,000
          </div>
        </div>

        {/* Etiquetas */}
        <div className="form-group">
          <label htmlFor="tagInput" className="form-label">
            Etiquetas (máximo 10)
          </label>
          <div className="tags-input-container">
            <input
              type="text"
              id="tagInput"
              name="tagInput"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyPress={handleKeyPress}
              className="form-input"
              placeholder="Escribe una etiqueta y presiona Enter..."
              disabled={loading || formData.tags.length >= 10}
            />
            <button
              type="button"
              onClick={handleAddTag}
              className="add-tag-btn"
              disabled={loading || !tagInput.trim() || formData.tags.length >= 10}
            >
              Agregar
            </button>
          </div>
          
          {/* Lista de etiquetas */}
          {formData.tags.length > 0 && (
            <div className="tags-list">
              {formData.tags.map((tag, index) => (
                <span key={index} className="tag-item">
                  #{tag}
                  <button
                    type="button"
                    onClick={() => handleRemoveTag(tag)}
                    className="remove-tag-btn"
                    disabled={loading}
                  >
                    ✕
                  </button>
                </span>
              ))}
            </div>
          )}
          
          {errors.tags && (
            <span className="error-message">{errors.tags}</span>
          )}
          
          <div className="tags-counter">
            {formData.tags.length}/10 etiquetas
          </div>
        </div>

        {/* Botones */}
        <div className="form-actions">
          <button
            type="button"
            onClick={onCancel}
            className="cancel-btn"
            disabled={loading}
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="submit-btn"
            disabled={loading}
          >
            {loading ? (
              <>
                <div className="loading-spinner-small"></div>
                {note ? 'Actualizando...' : 'Creando...'}
              </>
            ) : (
              note ? 'Actualizar Nota' : 'Crear Nota'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default NoteForm;