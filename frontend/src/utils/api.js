// Configuración base de la API - UPDATED FOR DEBUG
// Cambiar entre desarrollo local y producción
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://notesia.vercel.app/api'
  : 'http://localhost:8000/api'; // Usando backend local para desarrollo

// Función helper para hacer peticiones HTTP
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  

  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {

    const response = await fetch(url, config);
    

    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      
      // Manejar JWT expirado
      if (response.status === 401 || 
          (errorData.detail && errorData.detail.includes('JWT expired')) ||
          (errorData.message && errorData.message.includes('JWT expired'))) {
        // Limpiar datos de autenticación
        localStorage.removeItem('authToken');
        localStorage.removeItem('userEmail');
        
        // Redirigir al login
        window.location.href = '/login';
        return;
      }

      throw new Error(errorData.detail || `Error interno: ${JSON.stringify(errorData)}` || `HTTP error! status: ${response.status}`);
    }
    
    // Para respuestas DELETE exitosas, el backend puede no devolver contenido
    if (response.status === 204 || response.headers.get('content-length') === '0') {

      return null;
    }
    
    const responseData = await response.json();

    return responseData;
  } catch (error) {
    console.error('API Request Error:', error);
    throw error;
  }
};

// Servicios de autenticación
export const authAPI = {
  // Registro de usuario
  register: async (userData) => {
    return apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
        full_name: userData.full_name || `${userData.firstName} ${userData.lastName}`,
        username: userData.username || userData.email.split('@')[0] // Usar la parte antes del @ como username
      }),
    });
  },

  // Login de usuario
  login: async (credentials) => {
    return apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password
      }),
    });
  },

  // Obtener perfil del usuario (requiere token)
  getProfile: async (token) => {
    return apiRequest('/auth/me', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  },

  // Logout (si el backend lo requiere)
  logout: async (token) => {
    return apiRequest('/auth/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  },
};

// Servicios de notas (para uso futuro)
export const notesAPI = {
  // Obtener todas las notas del usuario
  getNotes: async (token) => {
    return apiRequest('/notes', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  },

  // Crear una nueva nota
  createNote: async (token, noteData) => {
  
    
    // Mapear estados del frontend al backend
    const statusMapping = {
      'draft': 'draft',
      'published': 'published', // Mantener published como published
      'active': 'published',    // El frontend usa 'active' pero el backend espera 'published'
      'archived': 'archived',
      'deleted': 'archived'     // Mapear deleted a archived
    };
    
    const processedData = {
      title: noteData.title || '',
      content: noteData.content || '',
      status: statusMapping[noteData.status] || 'draft',
      tags: Array.isArray(noteData.tags) ? noteData.tags : []
    };
    
    
    
    return apiRequest('/notes/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(processedData),
    });
  },

  // Actualizar una nota
  updateNote: async (token, noteId, noteData) => {
    
    
    // Mapear estados del frontend al backend
    const statusMapping = {
      'draft': 'draft',
      'published': 'published',  // Mapeo directo para published
      'active': 'published',     // El frontend usa 'active' pero el backend espera 'published'
      'archived': 'archived',
      'deleted': 'archived'      // Mapear deleted a archived
    };
    
    const processedData = {
      title: noteData.title || '',
      content: noteData.content || '',
      status: statusMapping[noteData.status] || 'draft',
      tags: Array.isArray(noteData.tags) ? noteData.tags : []
    };
    
  
    
    return apiRequest(`/notes/${noteId}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(processedData),
    });
  },

  // Eliminar una nota
  deleteNote: async (token, noteId) => {
    
    
    const result = await apiRequest(`/notes/${noteId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    
  
    return result;
  },
};

// Servicios de IA
export const aiAPI = {
  // Chat general con IA
  chat: async (token, prompt, context = null) => {
    return apiRequest('/ai/chat', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        prompt,
        context
      }),
    });
  },

  // Resumir una nota específica
  summarizeNote: async (token, noteId) => {
    return apiRequest('/ai/summarize', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        note_id: noteId
      }),
    });
  },

  // Mejorar una nota específica
  enhanceNote: async (token, noteId, enhancementType = 'improve') => {
    return apiRequest('/ai/enhance', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        note_id: noteId,
        enhancement_type: enhancementType
      }),
    });
  },

  // Generar nota desde prompt
  generateFromPrompt: async (token, prompt, title = null) => {
    return apiRequest('/ai/generate', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        prompt,
        title
      }),
    });
  },

  // Analizar todas las notas del usuario
  analyzeNotes: async (token) => {
    return apiRequest('/ai/analyze-notes', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
    });
  },
};

export default { authAPI, notesAPI, aiAPI };