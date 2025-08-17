import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { aiAPI } from '../utils/api';
import { RobotIcon } from './icons/index.js';
import './AIChat.css';

const AIChat = ({ isOpen, onClose }) => {
  const { token } = useAuth();
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: '¡Hola! Soy tu asistente especializado en tomar notas y organizar información. Puedo ayudarte a:\n\n📝 Resumir textos largos en puntos clave\n💡 Generar ideas y conceptos principales\n🎯 Extraer información importante de tus textos\n📋 Organizar y estructurar tus notas\n\n¿En qué puedo ayudarte hoy?',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError('');

    try {
      const response = await aiAPI.chat(token, inputMessage.trim());
      
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: response.response || 'Lo siento, no pude procesar tu mensaje.',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      console.error('Error in AI chat:', err);
      setError('Error al comunicarse con la IA. Por favor, intenta de nuevo.');
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo.',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        type: 'ai',
        content: '¡Hola! Soy tu asistente especializado en tomar notas y organizar información. Puedo ayudarte a:\n\n📝 Resumir textos largos en puntos clave\n💡 Generar ideas y conceptos principales\n🎯 Extraer información importante de tus textos\n📋 Organizar y estructurar tus notas\n\n¿En qué puedo ayudarte hoy?',
        timestamp: new Date()
      }
    ]);
    setError('');
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (!isOpen) return null;

  return (
    <div className="ai-chat-overlay">
      <div className="ai-chat-container">
        {/* Header */}
        <div className="ai-chat-header">
          <div className="ai-chat-title">
            <RobotIcon size={20} />
            <span>Chat con IA</span>
          </div>
          <div className="ai-chat-actions">
            <button 
              className="clear-chat-btn"
              onClick={clearChat}
              title="Limpiar chat"
            >
              🗑️
            </button>
            <button 
              className="close-chat-btn"
              onClick={onClose}
              title="Cerrar chat"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="ai-chat-error">
            {error}
          </div>
        )}

        {/* Messages */}
        <div className="ai-chat-messages">
          {messages.map((message) => (
            <div 
              key={message.id} 
              className={`message ${message.type === 'user' ? 'user-message' : 'ai-message'}`}
            >
              <div className="message-content">
                {message.content}
              </div>
              <div className="message-time">
                {formatTime(message.timestamp)}
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message ai-message">
              <div className="message-content loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                IA está escribiendo...
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <form className="ai-chat-input-form" onSubmit={handleSendMessage}>
          <div className="ai-chat-input-container">
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Escribe tu mensaje aquí..."
              className="ai-chat-input"
              rows={1}
              disabled={isLoading}
            />
            <button 
              type="submit" 
              className="ai-chat-send-btn"
              disabled={!inputMessage.trim() || isLoading}
            >
              {isLoading ? '⏳' : '📤'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AIChat;