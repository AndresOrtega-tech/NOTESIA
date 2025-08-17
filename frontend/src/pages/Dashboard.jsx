import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { notesAPI } from '../utils/api';
import NotesList from '../components/NotesList';
import NoteForm from '../components/NoteForm';
import { NoteIcon, WarningIcon } from '../components/icons';
import './Dashboard.css';

const Dashboard = () => {
  const { user, token, logout } = useAuth();
  const navigate = useNavigate();
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  
  // Debug: Log cuando cambia showCreateForm
  useEffect(() => {
  
  }, [showCreateForm]);
  const [editingNote, setEditingNote] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchFilter, setSearchFilter] = useState('all'); // 'all', 'title', 'content'
  const [statusFilter, setStatusFilter] = useState('all');

  // Cargar notas al montar el componente
  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    loadNotes();
  }, [token, navigate]);

  const loadNotes = async () => {
    try {
      setLoading(true);
      setError('');
      const notesData = await notesAPI.getNotes(token);
      setNotes(notesData);
    } catch (err) {
      setError('Error al cargar las notas: ' + (err.message || 'Error desconocido'));
      console.error('Error loading notes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNote = async (noteData) => {
    try {
      const newNote = await notesAPI.createNote(token, noteData);
      setNotes(prevNotes => [newNote, ...prevNotes]);
      setShowCreateForm(false);
      setError('');
    } catch (err) {
      setError('Error al crear la nota: ' + (err.message || 'Error desconocido'));
      console.error('Error creating note:', err);
    }
  };

  const handleUpdateNote = async (noteId, noteData) => {
    try {
      const updatedNote = await notesAPI.updateNote(token, noteId, noteData);
      setNotes(prevNotes => 
        prevNotes.map(note => 
          note.id === noteId ? updatedNote : note
        )
      );
      setEditingNote(null);
      setError('');
    } catch (err) {
      setError('Error al actualizar la nota: ' + (err.message || 'Error desconocido'));
      console.error('Error updating note:', err);
    }
  };

  const handleDeleteNote = async (noteId) => {
    if (!window.confirm('¿Estás seguro de que quieres eliminar esta nota?')) {
      return;
    }

    try {
      await notesAPI.deleteNote(token, noteId);
      setNotes(notes.filter(note => note.id !== noteId));
    } catch (err) {
      setError('Error al eliminar la nota: ' + (err.message || 'Error desconocido'));
      console.error('Error deleting note:', err);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (err) {
      console.error('Error during logout:', err);
      // Forzar navegación incluso si hay error
      navigate('/login');
    }
  };

  const filteredNotes = notes.filter(note => {
    let matchesSearch = true;
    
    if (searchTerm.trim()) {
      const searchLower = searchTerm.toLowerCase();
      const titleMatch = (note.title || '').toLowerCase().includes(searchLower);
      const contentMatch = (note.content || '').toLowerCase().includes(searchLower);
      
      switch (searchFilter) {
        case 'title':
          matchesSearch = titleMatch;
          break;
        case 'content':
          matchesSearch = contentMatch;
          break;
        case 'all':
        default:
          matchesSearch = titleMatch || contentMatch;
          break;
      }
    }
    
    const matchesStatus = statusFilter === 'all' || note.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Cargando notas...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <h1 className="dashboard-title"><NoteIcon size={32} className="inline-icon" />NOTESIA</h1>
            <p className="welcome-text">Bienvenido, {user?.full_name || user?.email}</p>
          </div>
          <div className="header-right">
            <button 
              className="logout-btn"
              onClick={handleLogout}
              title="Cerrar sesión"
            >
              🚪 Salir
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        {/* Controls */}
        <div className="dashboard-controls">
          <div className="controls-left">
            <button 
              className="create-note-btn"
              onClick={() => {
        
                setShowCreateForm(true);
              }}
            >
              ➕ Nueva Nota
            </button>
          </div>
          
          <div className="controls-center">
            <div className="search-container">
              <input
                type="text"
                placeholder={`Buscar ${searchFilter === 'title' ? 'por título' : searchFilter === 'content' ? 'por contenido' : 'notas'}...`}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
              <select 
                value={searchFilter} 
                onChange={(e) => setSearchFilter(e.target.value)}
                className="search-filter"
                title="Tipo de búsqueda"
              >
                <option value="all">Todo</option>
                <option value="title">Título</option>
                <option value="content">Contenido</option>
              </select>
            </div>
          </div>

          <div className="controls-right">
            <select 
              value={statusFilter} 
              onChange={(e) => setStatusFilter(e.target.value)}
              className="status-filter"
            >
              <option value="all">Todas</option>
              <option value="draft">Borradores</option>
              <option value="published">Publicadas</option>
              <option value="archived">Archivadas</option>
            </select>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="error-message">
            <WarningIcon size={16} className="inline-icon" />{error}
            <button 
              className="retry-btn"
              onClick={loadNotes}
            >
              Reintentar
            </button>
          </div>
        )}

        {/* Notes Content */}
        <div className="dashboard-content">
          {showCreateForm && (
            <div className="modal-overlay">
              <div className="modal-content">
                <NoteForm
                  onSubmit={handleCreateNote}
                  onCancel={() => setShowCreateForm(false)}
                  title="Crear Nueva Nota"
                />
              </div>
            </div>
          )}

          {editingNote && (
            <div className="modal-overlay">
              <div className="modal-content">
                <NoteForm
                  note={editingNote}
                  onSubmit={(noteData) => handleUpdateNote(editingNote.id, noteData)}
                  onCancel={() => setEditingNote(null)}
                  title="Editar Nota"
                />
              </div>
            </div>
          )}

          <NotesList
            notes={filteredNotes}
            onEdit={setEditingNote}
            onDelete={handleDeleteNote}
            loading={loading}
          />
        </div>
      </main>
    </div>
  );
};

export default Dashboard;