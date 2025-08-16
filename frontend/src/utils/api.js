// Configuración base de la API
// Cambiar entre desarrollo local y producción
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://notesia.vercel.app/api'
  : 'https://notesia.vercel.app/api'; // Usando Vercel para desarrollo también

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
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
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
        first_name: userData.firstName,
        last_name: userData.lastName
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
    return apiRequest('/notes/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  },

  // Crear una nueva nota
  createNote: async (token, noteData) => {
    return apiRequest('/notes/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(noteData),
    });
  },

  // Actualizar una nota
  updateNote: async (token, noteId, noteData) => {
    return apiRequest(`/notes/${noteId}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(noteData),
    });
  },

  // Eliminar una nota
  deleteNote: async (token, noteId) => {
    return apiRequest(`/notes/${noteId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  },
};

export default { authAPI, notesAPI };