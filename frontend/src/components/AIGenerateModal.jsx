import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { aiAPI, notesAPI } from '../utils/api';
import { RobotIcon, NoteIcon } from './icons/index.js';
import './AIGenerateModal.css';

const AIGenerateModal = ({ isOpen, onClose, onNoteCreated }) => {
  const { token } = useAuth();
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] = useState('');
  const [error, setError] = useState('');
  const [step, setStep] = useState('prompt'); // 'prompt', 'preview', 'saving'

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!prompt.trim() || isGenerating) return;

    setIsGenerating(true);
    setError('');
    setGeneratedContent('');

    try {
      const response = await aiAPI.generateFromPrompt(token, prompt.trim());
      
      if (response.note) {
        setGeneratedContent(response.note);
        setStep('preview');
      } else {
        throw new Error('No se pudo generar el contenido');
      }
    } catch (err) {
      console.error('Error generating content:', err);
      setError('Error al generar la nota: ' + (err.message || 'Error desconocido'));
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSaveNote = async () => {
    if (!generatedContent.trim()) return;

    setStep('saving');
    setError('');

    try {
      // Extraer título del contenido generado (primera línea o primeras palabras)
      const lines = generatedContent.split('\n').filter(line => line.trim());
      const title = lines[0] ? lines[0].substring(0, 100) : 'Nota generada por IA';
      
      const noteData = {
        title: title,
        content: generatedContent,
        status: 'draft'
      };

      const newNote = await notesAPI.createNote(token, noteData);
      
      // Notificar al componente padre que se creó una nueva nota
      if (onNoteCreated) {
        onNoteCreated(newNote);
      }

      // Resetear el modal
      handleClose();
    } catch (err) {
      console.error('Error saving note:', err);
      setError('Error al guardar la nota: ' + (err.message || 'Error desconocido'));
      setStep('preview');
    }
  };

  const handleClose = () => {
    setPrompt('');
    setGeneratedContent('');
    setError('');
    setStep('prompt');
    onClose();
  };

  const handleBackToPrompt = () => {
    setStep('prompt');
    setError('');
  };

  if (!isOpen) return null;

  return (
    <div className="ai-generate-overlay">
      <div className="ai-generate-modal">
        {/* Header */}
        <div className="ai-generate-header">
          <div className="ai-generate-title">
            <RobotIcon size={20} />
            <span>Generar Nota con IA</span>
          </div>
          <button 
            className="close-btn"
            onClick={handleClose}
            title="Cerrar"
          >
            ✕
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="ai-generate-error">
            {error}
          </div>
        )}

        {/* Content */}
        <div className="ai-generate-content">
          {step === 'prompt' && (
            <div className="prompt-step">
              <h3>Describe qué tipo de nota quieres crear</h3>
              <p className="step-description">
                Escribe un prompt detallado y la IA generará una nota completa para ti.
              </p>
              
              <form onSubmit={handleGenerate}>
                <div className="prompt-input-container">
                  <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Ejemplo: Crea una nota sobre los beneficios del ejercicio regular, incluyendo aspectos físicos y mentales..."
                    className="prompt-input"
                    rows={6}
                    disabled={isGenerating}
                    autoFocus
                  />
                </div>
                
                <div className="prompt-actions">
                  <button 
                    type="button" 
                    className="btn-secondary"
                    onClick={handleClose}
                    disabled={isGenerating}
                  >
                    Cancelar
                  </button>
                  <button 
                    type="submit" 
                    className="btn-primary"
                    disabled={!prompt.trim() || isGenerating}
                  >
                    {isGenerating ? (
                      <>
                        <div className="spinner"></div>
                        Generando...
                      </>
                    ) : (
                      <>
                        <RobotIcon size={16} />
                        Generar Nota
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>
          )}

          {step === 'preview' && (
            <div className="preview-step">
              <h3>Vista previa de la nota generada</h3>
              <p className="step-description">
                Revisa el contenido generado y guárdalo como una nueva nota.
              </p>
              
              <div className="generated-content-container">
                <div className="generated-content">
                  {generatedContent.split('\n').map((line, index) => (
                    <p key={index}>{line || '\u00A0'}</p>
                  ))}
                </div>
              </div>
              
              <div className="preview-actions">
                <button 
                  type="button" 
                  className="btn-secondary"
                  onClick={handleBackToPrompt}
                >
                  ← Volver al Prompt
                </button>
                <button 
                  type="button" 
                  className="btn-primary"
                  onClick={handleSaveNote}
                >
                  <NoteIcon size={16} />
                  Guardar Nota
                </button>
              </div>
            </div>
          )}

          {step === 'saving' && (
            <div className="saving-step">
              <div className="saving-content">
                <div className="spinner large"></div>
                <h3>Guardando nota...</h3>
                <p>Por favor espera mientras guardamos tu nueva nota.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIGenerateModal;