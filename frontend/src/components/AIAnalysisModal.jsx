import React from 'react';
import ReactMarkdown from 'react-markdown';
import { RobotIcon } from './icons/index.js';
import './AIAnalysisModal.css';

const AIAnalysisModal = ({ isOpen, onClose, analysisData, loading }) => {
  if (!isOpen) return null;

  const formatAnalysisSection = (title, content) => {
    if (!content) return null;
    
    return (
      <div className="analysis-section">
        <h4 className="analysis-section-title">{title}</h4>
        <div className="analysis-section-content">
          {typeof content === 'string' ? (
            content.split('\n').map((line, index) => (
              <p key={index}>{line || '\u00A0'}</p>
            ))
          ) : (
            <p>{JSON.stringify(content, null, 2)}</p>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="ai-analysis-overlay">
      <div className="ai-analysis-modal">
        {/* Header */}
        <div className="ai-analysis-header">
          <div className="ai-analysis-title">
            <RobotIcon size={20} />
            <span>Análisis de Notas con IA</span>
          </div>
          <button 
            className="close-btn"
            onClick={onClose}
            title="Cerrar"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="ai-analysis-content">
          {loading ? (
            <div className="analysis-loading">
              <div className="spinner large"></div>
              <h3>Analizando tus notas...</h3>
              <p>La IA está procesando todas tus notas para generar insights útiles.</p>
            </div>
          ) : analysisData ? (
            <div className="analysis-results">
              <div className="analysis-intro">
                <h3>📊 Resumen del Análisis</h3>
                <p>Aquí tienes un análisis completo de tus notas generado por IA:</p>
              </div>

              <div className="analysis-sections">
                {formatAnalysisSection('📈 Estadísticas Generales', analysisData.statistics)}
                {formatAnalysisSection('🏷️ Temas Principales', analysisData.main_themes)}
                {formatAnalysisSection('💡 Insights y Patrones', analysisData.insights)}
                {formatAnalysisSection('📝 Resumen General', analysisData.summary)}
                {formatAnalysisSection('🎯 Recomendaciones', analysisData.recommendations)}
                {formatAnalysisSection('🔍 Análisis Detallado', analysisData.analysis)}
                
                {/* Fallback para mostrar toda la respuesta si no tiene estructura específica */}
                {!analysisData.statistics && !analysisData.main_themes && !analysisData.insights && (
                  <div className="analysis-section">
                    <h4 className="analysis-section-title">📋 Análisis Completo</h4>
                    <div className="analysis-section-content">
                      {typeof analysisData === 'string' ? (
                        <ReactMarkdown>{analysisData}</ReactMarkdown>
                      ) : (
                        <pre>{JSON.stringify(analysisData, null, 2)}</pre>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="analysis-error">
              <h3>❌ No hay datos de análisis</h3>
              <p>No se pudo obtener el análisis de tus notas. Por favor, intenta de nuevo.</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="ai-analysis-footer">
          <button 
            className="btn-primary"
            onClick={onClose}
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIAnalysisModal;