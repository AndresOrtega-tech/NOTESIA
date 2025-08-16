import React from 'react';

const Header = ({ title = "Notesia" }) => {
  return (
    <header style={{
      padding: '1rem',
      backgroundColor: '#f8f9fa',
      borderBottom: '1px solid #dee2e6',
      textAlign: 'center'
    }}>
      <h1 style={{
        margin: 0,
        color: '#333',
        fontSize: '2rem'
      }}>
        {title}
      </h1>
    </header>
  );
};

export default Header;