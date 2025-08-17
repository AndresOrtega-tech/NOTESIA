import React from 'react';
import { useNavigate } from 'react-router-dom';
import { NoteIcon, SearchIcon, RobotIcon } from '../components/icons';
import { useAuth } from '../hooks/useAuth.jsx';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="home-container">
      <button
        onClick={handleLogout}
        className="logout-button"
      >
        Cerrar Sesión
      </button>
      <main className="home-main">
        <h2 className="home-title">Tu aplicación de notas inteligente</h2>
        <p className="home-description">
          Bienvenido, <strong>{user?.email || 'Usuario'}</strong>! Notesia es una aplicación moderna para gestionar tus notas con 
          funcionalidades de inteligencia artificial integradas.
        </p>
        <div className="features-grid">
          <div className="feature-card">
            <h3 className="feature-title"><NoteIcon size={20} className="inline-icon" />Crear Notas</h3>
            <p className="feature-description">Crea y organiza tus notas de manera sencilla</p>
          </div>
          <div className="feature-card">
            <h3 className="feature-title"><RobotIcon size={20} className="inline-icon" />IA Integrada</h3>
            <p className="feature-description">Mejora tus notas con inteligencia artificial</p>
          </div>
          <div className="feature-card">
            <h3 className="feature-title"><SearchIcon size={20} className="inline-icon" />Búsqueda Avanzada</h3>
            <p className="feature-description">Encuentra tus notas rápidamente</p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;