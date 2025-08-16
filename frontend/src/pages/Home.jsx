import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth.jsx';
import Header from '../components/Header';

const Home = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div>
      <Header title="Bienvenido a Notesia" />
      <div style={{
        position: 'absolute',
        top: '1rem',
        right: '1rem'
      }}>
        <button
          onClick={handleLogout}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Cerrar Sesión
        </button>
      </div>
      <main style={{
        padding: '2rem',
        maxWidth: '800px',
        margin: '0 auto'
      }}>
        <h2>Tu aplicación de notas inteligente</h2>
        <p>
          Bienvenido, <strong>{user?.email || 'Usuario'}</strong>! Notesia es una aplicación moderna para gestionar tus notas con 
          funcionalidades de inteligencia artificial integradas.
        </p>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '1rem',
          marginTop: '2rem'
        }}>
          <div style={{
            padding: '1rem',
            border: '1px solid #ddd',
            borderRadius: '8px',
            backgroundColor: '#f8f9fa'
          }}>
            <h3>📝 Crear Notas</h3>
            <p>Crea y organiza tus notas de manera sencilla</p>
          </div>
          <div style={{
            padding: '1rem',
            border: '1px solid #ddd',
            borderRadius: '8px',
            backgroundColor: '#f8f9fa'
          }}>
            <h3>🤖 IA Integrada</h3>
            <p>Mejora tus notas con inteligencia artificial</p>
          </div>
          <div style={{
            padding: '1rem',
            border: '1px solid #ddd',
            borderRadius: '8px',
            backgroundColor: '#f8f9fa'
          }}>
            <h3>🔍 Búsqueda Avanzada</h3>
            <p>Encuentra tus notas rápidamente</p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;