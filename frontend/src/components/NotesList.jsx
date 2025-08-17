import React from 'react';
import './NotesList.css';

const NotesList = ({ notes, onEdit, onDelete, loading }) => {
  if (loading) {
    return (
      <div className="notes-loading">
        <div className="loading-spinner"></div>
        <p>Cargando notas...</p>
      </div>
    );
  }

  if (!notes || notes.length === 0) {
    return (
      <div className="notes-empty">
        <div className="empty-icon">📝</div>
        <h3>No hay notas aún</h3>
        <p>¡Crea tu primera nota para comenzar!</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'draft':
        return '📝';
      case 'published':
        return '✅';
      case 'archived':
        return '📦';
      default:
        return '📄';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'draft':
        return 'Borrador';
      case 'published':
        return 'Publicada';
      case 'archived':
        return 'Archivada';
      default:
        return 'Sin estado';
    }
  };

  const truncateContent = (content, maxLength = 150) => {
    if (content.length <= maxLength) return content;
    return content.substring(0, maxLength) + '...';
  };

  return (
    <div className="notes-list">
      <div className="notes-grid">
        {notes.map((note) => (
          <div key={note.id} className={`note-card note-status-${note.status}`}>
            {/* Header de la nota */}
            <div className="note-header">
              <div className="note-status">
                <span className="status-icon">{getStatusIcon(note.status)}</span>
                <span className="status-text">{getStatusText(note.status)}</span>
              </div>
              <div className="note-actions">
                <button
                  className="action-btn edit-btn"
                  onClick={() => onEdit(note)}
                  title="Editar nota"
                >
                  ✏️
                </button>
                <button
                  className="action-btn delete-btn"
                  onClick={() => onDelete(note.id)}
                  title="Eliminar nota"
                >
                  🗑️
                </button>
              </div>
            </div>

            {/* Contenido de la nota */}
            <div className="note-content">
              <h3 className="note-title">{note.title}</h3>
              <p className="note-text">{truncateContent(note.content)}</p>
            </div>

            {/* Tags */}
            {note.tags && note.tags.length > 0 && (
              <div className="note-tags">
                {note.tags.slice(0, 3).map((tag, index) => (
                  <span key={index} className="note-tag">
                    #{tag}
                  </span>
                ))}
                {note.tags.length > 3 && (
                  <span className="note-tag more-tags">
                    +{note.tags.length - 3}
                  </span>
                )}
              </div>
            )}

            {/* Footer con fechas */}
            <div className="note-footer">
              <div className="note-dates">
                <div className="note-date">
                  <span className="date-label">Creada:</span>
                  <span className="date-value">{formatDate(note.created_at)}</span>
                </div>
                {note.updated_at !== note.created_at && (
                  <div className="note-date">
                    <span className="date-label">Actualizada:</span>
                    <span className="date-value">{formatDate(note.updated_at)}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NotesList;