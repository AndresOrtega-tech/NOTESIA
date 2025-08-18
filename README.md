# 📝 NOTESIA - Generador de Ideas con Gemini

> Una aplicación web Full-Stack que combina gestión de notas con inteligencia artificial para la generación de contenido dinámico.

## 📋 Descripción del Proyecto

NOTESIA es una **aplicación de portafolio** que demuestra habilidades completas en desarrollo Full-Stack. El proyecto integra:

- **Backend**: Desarrollo de APIs RESTful propias con FastAPI
- **Frontend**: Aplicación React con manejo de estado y comunicación con APIs
- **Base de Datos**: Conexión y gestión de datos con PostgreSQL
- **APIs de Terceros**: Integración con la API de Gemini para IA
- **Operaciones CRUD**: Implementación completa de Create, Read, Update, Delete
- **Autenticación**: Sistema de autenticación JWT personalizado
- **Despliegue**: Configuración de producción en plataformas cloud

## 🛠️ Tecnologías Utilizadas y Justificación

| Categoría | Tecnología | Justificación |
|-----------|------------|---------------|
| **Frontend** | React + Vite | Framework moderno para SPAs con excelente ecosistema y rendimiento |
| **Backend** | Python + FastAPI | Framework rápido con documentación automática y tipado estático |
| **Base de Datos** | Supabase (PostgreSQL) | Plataforma fácil e intuitiva para proyectos personales con auth integrado |
| **IA** | API de Gemini | API de terceros moderna para demostrar integración con servicios externos |
| **Despliegue** | Vercel | Plataforma fácil e intuitiva para subir proyectos personales y prototipos |
| **Autenticación** | JWT | Estándar de la industria para autenticación stateless |

### 🎯 ¿Por qué estas tecnologías?

**Vercel**: Elegido por ser una plataforma extremadamente fácil e intuitiva para subir proyectos personales o prototipos. Ofrece:
- Despliegue automático desde Git
- Serverless functions para el backend
- CDN global para el frontend
- Configuración mínima requerida

**Supabase**: Seleccionado por ser una plataforma fácil e intuitiva que proporciona:
- Base de datos PostgreSQL gestionada
- Sistema de autenticación integrado
- APIs automáticas
- Dashboard intuitivo para gestión

## 🏗️ Arquitectura del Proyecto

### 📁 Estructura de Archivos Importantes

```
NOTESIA/
├── backend/
│   ├── app/
│   │   ├── main.py              # Punto de entrada de la aplicación
│   │   ├── config.py            # Configuración y variables de entorno
│   │   ├── database.py          # Conexión a Supabase/PostgreSQL
│   │   ├── models/
│   │   │   ├── user.py          # Modelos Pydantic para usuarios
│   │   │   └── note.py          # Modelos Pydantic para notas
│   │   ├── routers/
│   │   │   ├── auth.py          # Endpoints de autenticación
│   │   │   ├── notes.py         # Endpoints CRUD de notas
│   │   │   └── gemini.py        # Endpoints de IA con Gemini
│   │   └── utils/
│   │       └── auth.py          # Utilidades de autenticación JWT
│   ├── requirements.txt         # Dependencias de Python
│   └── vercel.json             # Configuración de despliegue
└── frontend/
    ├── src/
    │   ├── App.jsx             # Componente principal
    │   ├── components/
    │   │   ├── NotesList.jsx   # Lista de notas
    │   │   ├── NoteForm.jsx    # Formulario de notas
    │   │   ├── AIChat.jsx      # Chat con IA
    │   │   └── icons/          # Iconos SVG personalizados
    │   ├── pages/
    │   │   ├── Home.jsx        # Página de inicio
    │   │   ├── Login.jsx       # Página de login
    │   │   ├── Register.jsx    # Página de registro
    │   │   └── Dashboard.jsx   # Dashboard principal
    │   ├── hooks/
    │   │   └── useAuth.js      # Hook personalizado para autenticación
    │   └── utils/
    │       └── api.js          # Configuración de APIs
    ├── package.json            # Dependencias de Node.js
    └── vercel.json            # Configuración de despliegue
```

### 🎨 Frontend (React)

**Ubicación**: `/frontend/src/`

**Características principales:**
- **SPA (Single Page Application)** con React Router
- **Gestión de Estado**: Context API para autenticación global
- **Hooks Personalizados**: `useAuth` para manejo de sesión
- **Componentes Modulares**: Separación clara de responsabilidades
- **Comunicación con APIs**: Axios para peticiones HTTP

**Archivos Clave:**
- `App.jsx`: Configuración de rutas y contexto global
- `hooks/useAuth.js`: Lógica de autenticación reutilizable
- `utils/api.js`: Configuración centralizada de APIs
- `components/`: Componentes reutilizables de UI

### ⚙️ Backend (FastAPI)

**Ubicación**: `/backend/app/`

**Arquitectura Modular:**
- **Routers**: Separación de endpoints por funcionalidad
- **Models**: Validación de datos con Pydantic
- **Utils**: Funciones auxiliares reutilizables
- **Config**: Gestión centralizada de configuración

## 📚 Documentación Completa de la API

### 🔐 Sistema de Autenticación

**Ubicación**: `/backend/app/routers/auth.py` y `/backend/app/utils/auth.py`

**Características:**
- Autenticación basada en JWT (JSON Web Tokens)
- Hashing seguro de contraseñas con bcrypt
- Tokens con expiración configurable
- Middleware de protección de rutas

#### Endpoints de Autenticación

**POST /auth/register**
- **Archivo**: `backend/app/routers/auth.py:15-45`
- **Descripción**: Registro de nuevos usuarios con validación
- **Validaciones**:
  - Email único y formato válido
  - Contraseña mínimo 6 caracteres
  - Username único (generado automáticamente si no se proporciona)
- **Body**:
  ```json
  {
    "email": "usuario@ejemplo.com",
    "password": "contraseña123",
    "full_name": "Nombre Completo",
    "username": "usuario" // Opcional
  }
  ```
- **Respuesta Exitosa (201)**:
  ```json
  {
    "id": "uuid",
    "email": "usuario@ejemplo.com",
    "full_name": "Nombre Completo",
    "username": "usuario",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
  ```

**POST /auth/login**
- **Archivo**: `backend/app/routers/auth.py:47-75`
- **Descripción**: Autenticación de usuarios existentes
- **Validaciones**:
  - Email y contraseña requeridos
  - Verificación de credenciales contra base de datos
- **Body**:
  ```json
  {
    "email": "usuario@ejemplo.com",
    "password": "contraseña123"
  }
  ```
- **Respuesta Exitosa (200)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "id": "uuid",
      "email": "usuario@ejemplo.com",
      "full_name": "Nombre Completo",
      "username": "usuario"
    }
  }
  ```

**GET /auth/me**
- **Archivo**: `backend/app/routers/auth.py:77-85`
- **Descripción**: Obtener información del usuario autenticado
- **Headers**: `Authorization: Bearer <token>`
- **Respuesta (200)**:
  ```json
  {
    "id": "uuid",
    "email": "usuario@ejemplo.com",
    "full_name": "Nombre Completo",
    "username": "usuario",
    "is_active": true
  }
  ```

**POST /auth/logout**
- **Archivo**: `backend/app/routers/auth.py:87-95`
- **Descripción**: Cerrar sesión (invalidación del token en frontend)
- **Headers**: `Authorization: Bearer <token>`
- **Respuesta (200)**: `{"message": "Logout successful"}`

### 📝 Gestión de Notas (CRUD Completo)

**Ubicación**: `/backend/app/routers/notes.py`

#### Modelos y Enumeraciones

**Archivo**: `/backend/app/models/note.py`

**NoteStatus (Enum)**:
```python
class NoteStatus(str, Enum):
    draft = "draft"        # Borrador - nota en desarrollo
    published = "published" # Publicada - nota finalizada
    archived = "archived"   # Archivada - nota guardada pero no activa
```

**Modelos Pydantic**:
- `NoteBase`: Campos base compartidos
- `NoteCreate`: Validación para creación
- `NoteUpdate`: Validación para actualización (campos opcionales)
- `NoteInDB`: Representación en base de datos
- `Note`: Respuesta de API
- `NoteWithAI`: Nota con campos de IA opcionales

#### Endpoints de Notas

**GET /notes**
- **Archivo**: `backend/app/routers/notes.py:25-45`
- **Descripción**: Listar todas las notas del usuario autenticado
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters**:
  - `skip`: int = 0 (paginación)
  - `limit`: int = 100 (máximo por página)
- **Validaciones**:
  - Usuario autenticado requerido
  - Solo notas del usuario actual
- **Respuesta (200)**:
  ```json
  [
    {
      "id": "uuid",
      "title": "Mi Primera Nota",
      "content": "Contenido de la nota...",
      "tags": ["personal", "ideas"],
      "status": "published",
      "user_id": "uuid",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
  ```

**POST /notes**
- **Archivo**: `backend/app/routers/notes.py:47-70`
- **Descripción**: Crear nueva nota
- **Headers**: `Authorization: Bearer <token>`
- **Validaciones**:
  - Título requerido (mín. 1 carácter)
  - Contenido requerido (mín. 1 carácter)
  - Tags opcionales (array de strings)
  - Status por defecto: "draft"
- **Body**:
  ```json
  {
    "title": "Nueva Nota",
    "content": "Contenido de la nota",
    "tags": ["tag1", "tag2"],
    "status": "draft"
  }
  ```
- **Respuesta (201)**: Objeto de nota creada

**GET /notes/{note_id}**
- **Archivo**: `backend/app/routers/notes.py:72-85`
- **Descripción**: Obtener nota específica
- **Headers**: `Authorization: Bearer <token>`
- **Validaciones**:
  - UUID válido requerido
  - Nota debe pertenecer al usuario autenticado
- **Respuesta (200)**: Objeto de nota
- **Errores**: 404 si no existe o no pertenece al usuario

**PUT /notes/{note_id}**
- **Archivo**: `backend/app/routers/notes.py:87-110`
- **Descripción**: Actualizar nota existente
- **Headers**: `Authorization: Bearer <token>`
- **Validaciones**:
  - UUID válido requerido
  - Nota debe pertenecer al usuario
  - Campos opcionales (solo se actualizan los enviados)
- **Body** (todos los campos opcionales):
  ```json
  {
    "title": "Título Actualizado",
    "content": "Contenido actualizado",
    "tags": ["nuevo_tag"],
    "status": "published"
  }
  ```
- **Respuesta (200)**: Objeto de nota actualizada

**DELETE /notes/{note_id}**
- **Archivo**: `backend/app/routers/notes.py:112-125`
- **Descripción**: Eliminar nota
- **Headers**: `Authorization: Bearer <token>`
- **Validaciones**:
  - UUID válido requerido
  - Nota debe pertenecer al usuario
- **Respuesta (200)**: `{"message": "Note deleted successfully"}`

### 🤖 Inteligencia Artificial (Integración con Gemini)

**Ubicación**: `/backend/app/routers/gemini.py`

**Configuración**: API Key de Gemini en variables de entorno

#### Endpoints de IA

**POST /ai/chat**
- **Archivo**: `backend/app/routers/gemini.py:25-50`
- **Descripción**: Chat general con asistente de IA especializado en notas
- **Headers**: `Authorization: Bearer <token>`
- **Validaciones**:
  - Prompt requerido (mín. 1 carácter)
  - Máximo 1000 caracteres por prompt
- **Body**:
  ```json
  {
    "prompt": "¿Puedes ayudarme con ideas para organizar mis notas?"
  }
  ```
- **Respuesta (200)**:
  ```json
  {
    "response": "¡Por supuesto! Aquí tienes algunas ideas para organizar tus notas..."
  }
  ```

**POST /ai/summarize**
- **Archivo**: `backend/app/routers/gemini.py:52-80`
- **Descripción**: Generar resumen inteligente de una nota
- **Headers**: `Authorization: Bearer <token>`
- **Validaciones**:
  - note_id UUID válido requerido
  - Nota debe pertenecer al usuario
  - Nota debe tener contenido suficiente
- **Body**:
  ```json
  {
    "note_id": "uuid-de-la-nota"
  }
  ```
- **Respuesta (200)**:
  ```json
  {
    "summary": "Resumen conciso de los puntos principales de la nota..."
  }
  ```

**POST /ai/enhance**
- **Archivo**: `backend/app/routers/gemini.py:82-115`
- **Descripción**: Mejorar contenido de nota existente
- **Headers**: `Authorization: Bearer <token>`
- **Validaciones**:
  - note_id UUID válido requerido
  - enhancement_type debe ser valor válido del enum
- **Enhancement Types (Enum)**:
  - `grammar`: Corrección gramatical y ortográfica
  - `style`: Mejora de estilo y fluidez
  - `expand`: Expansión del contenido con más detalles
  - `clarity`: Mejora de claridad y estructura
- **Body**:
  ```json
  {
    "note_id": "uuid-de-la-nota",
    "enhancement_type": "grammar"
  }
  ```
- **Respuesta (200)**:
  ```json
  {
    "enhanced_content": "Contenido mejorado con correcciones gramaticales..."
  }
  ```

**POST /ai/generate**
- **Archivo**: `backend/app/routers/gemini.py:117-145`
- **Descripción**: Generar contenido de nota desde prompt
- **Headers**: `Authorization: Bearer <token>`
- **Validaciones**:
  - Prompt requerido (mín. 5 caracteres)
  - Título opcional (se genera automáticamente si no se proporciona)
- **Body**:
  ```json
  {
    "prompt": "Escribe sobre los beneficios de la meditación diaria",
    "title": "Beneficios de la Meditación"
  }
  ```
- **Respuesta (200)**:
  ```json
  {
    "title": "Beneficios de la Meditación",
    "content": "La meditación diaria ofrece numerosos beneficios..."
  }
  ```

**POST /ai/analyze-notes**
- **Archivo**: `backend/app/routers/gemini.py:147-175`
- **Descripción**: Análisis inteligente de todas las notas del usuario
- **Headers**: `Authorization: Bearer <token>`
- **Validaciones**:
  - Usuario debe tener al menos una nota
- **Respuesta (200)**:
  ```json
  {
    "analysis": "Análisis detallado: Tus notas muestran un patrón de interés en tecnología y desarrollo personal. Se identifican 3 temas principales: programación (40%), productividad (35%), y aprendizaje (25%). Sugerencia: considera crear categorías más específicas para mejor organización."
  }
  ```

### 🛡️ Validaciones y Seguridad

#### Validaciones de Datos (Pydantic)

**Ubicación**: `/backend/app/models/`

**Validaciones de Usuario**:
- Email: formato válido y único
- Password: mínimo 6 caracteres
- Username: único, alfanumérico, 3-20 caracteres
- Full_name: 1-100 caracteres

**Validaciones de Nota**:
- Title: 1-200 caracteres, requerido
- Content: 1-10000 caracteres, requerido
- Tags: array opcional, máximo 10 tags, cada tag máximo 50 caracteres
- Status: debe ser valor válido del enum NoteStatus

#### Seguridad

**JWT (JSON Web Tokens)**:
- **Ubicación**: `/backend/app/utils/auth.py`
- Algoritmo: HS256
- Expiración: 60 minutos (configurable)
- Claims: user_id, exp, iat

**Protección de Rutas**:
- Dependency injection con `get_current_user_dependency`
- Verificación automática de tokens en endpoints protegidos
- Validación de pertenencia de recursos (notas del usuario actual)

**Hashing de Contraseñas**:
- bcrypt para hashing seguro
- Salt automático para cada contraseña

### 📊 Códigos de Estado HTTP

| Código | Descripción | Casos de Uso |
|--------|-------------|--------------|
| **200** | OK | Operaciones exitosas (GET, PUT, DELETE) |
| **201** | Created | Recursos creados (POST register, POST notes) |
| **400** | Bad Request | Datos inválidos, formato incorrecto |
| **401** | Unauthorized | Token faltante, inválido o expirado |
| **403** | Forbidden | Sin permisos para el recurso |
| **404** | Not Found | Recurso no existe o no pertenece al usuario |
| **422** | Unprocessable Entity | Error de validación de Pydantic |
| **500** | Internal Server Error | Error del servidor o API externa |

### 🗄️ Base de Datos (Supabase/PostgreSQL)

**Configuración**: `/backend/app/database.py`

#### Estructura de Tablas

**Tabla `auth.users` (Gestionada por Supabase)**:
```sql
- id: UUID PRIMARY KEY
- email: VARCHAR UNIQUE NOT NULL
- encrypted_password: VARCHAR NOT NULL
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
- email_confirmed_at: TIMESTAMP
- last_sign_in_at: TIMESTAMP
```

**Tabla `public.users` (Personalizada)**:
```sql
- id: UUID PRIMARY KEY REFERENCES auth.users(id)
- full_name: VARCHAR(100) NOT NULL
- username: VARCHAR(50) UNIQUE NOT NULL
- is_active: BOOLEAN DEFAULT true
- created_at: TIMESTAMP DEFAULT NOW()
- updated_at: TIMESTAMP DEFAULT NOW()
```

**Tabla `public.notes`**:
```sql
- id: UUID PRIMARY KEY DEFAULT gen_random_uuid()
- title: VARCHAR(200) NOT NULL
- content: TEXT NOT NULL
- tags: TEXT[] DEFAULT '{}'
- status: VARCHAR(20) DEFAULT 'draft'
- user_id: UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE
- created_at: TIMESTAMP DEFAULT NOW()
- updated_at: TIMESTAMP DEFAULT NOW()
```

#### Políticas de Seguridad (RLS - Row Level Security)

```sql
-- Los usuarios solo pueden ver sus propias notas
CREATE POLICY "Users can view own notes" ON public.notes
    FOR SELECT USING (auth.uid() = user_id);

-- Los usuarios solo pueden insertar notas para sí mismos
CREATE POLICY "Users can insert own notes" ON public.notes
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Los usuarios solo pueden actualizar sus propias notas
CREATE POLICY "Users can update own notes" ON public.notes
    FOR UPDATE USING (auth.uid() = user_id);

-- Los usuarios solo pueden eliminar sus propias notas
CREATE POLICY "Users can delete own notes" ON public.notes
    FOR DELETE USING (auth.uid() = user_id);
```

## 🚀 Configuración y Despliegue

### 📋 Variables de Entorno

**Backend** (`.env`):
```env
# Supabase Configuration
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_supabase_anon_key
SUPABASE_SERVICE_KEY=tu_supabase_service_key

# JWT Configuration
JWT_SECRET_KEY=tu_jwt_secret_super_seguro
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Gemini AI Configuration
GEMINI_API_KEY=tu_gemini_api_key

# Environment
ENVIRONMENT=production
```

**Frontend** (`.env`):
```env
VITE_API_URL=https://tu-dominio.vercel.app/api
```

### 🔧 Despliegue en Vercel

**Configuración Backend** (`/backend/vercel.json`):
```json
{
  "functions": {
    "app/main.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/app/main.py"
    }
  ]
}
```

**Configuración Frontend** (`/frontend/vercel.json`):
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### 📦 Dependencias

**Backend** (`requirements.txt`):
```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
supabase==2.0.0
google-generativeai==0.3.0
pydantic==2.5.0
python-dotenv==1.0.0
```

**Frontend** (`package.json`):
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.3",
    "vite": "^4.4.5"
  }
}
```

## 🌟 Características del Proyecto como Portafolio

### 🎯 Habilidades Demostradas

#### Backend Development
- **APIs RESTful**: Diseño e implementación de endpoints siguiendo principios REST
- **Autenticación JWT**: Sistema de autenticación seguro y escalable
- **Validación de Datos**: Uso de Pydantic para validación robusta
- **Arquitectura Modular**: Separación clara de responsabilidades
- **Integración de APIs**: Consumo de APIs de terceros (Gemini)
- **Base de Datos**: Diseño de esquemas y relaciones
- **Seguridad**: Implementación de medidas de seguridad (hashing, RLS)

#### Frontend Development
- **React Moderno**: Hooks, Context API, componentes funcionales
- **Gestión de Estado**: Manejo eficiente del estado global
- **Comunicación HTTP**: Integración con APIs backend
- **Routing**: Navegación SPA con React Router
- **UI/UX**: Interfaz intuitiva y responsive

#### DevOps y Despliegue
- **Configuración de Producción**: Setup para entornos de producción
- **Variables de Entorno**: Gestión segura de configuración
- **Despliegue Automatizado**: CI/CD con Vercel
- **Monitoreo**: Logging y manejo de errores

#### Integración de Servicios
- **Supabase**: Base de datos como servicio
- **Gemini AI**: Integración con servicios de IA
- **Vercel**: Plataforma de despliegue serverless

### 🔍 Casos de Uso Demostrados

1. **CRUD Completo**: Operaciones completas de Create, Read, Update, Delete
2. **Autenticación Completa**: Registro, login, logout, protección de rutas
3. **Integración de IA**: Uso práctico de APIs de inteligencia artificial
4. **Gestión de Estado**: Manejo complejo de estado en aplicaciones web
5. **Validación Robusta**: Validación tanto en frontend como backend
6. **Seguridad**: Implementación de mejores prácticas de seguridad

## 🤝 Guía de Uso

### 🚪 Primeros Pasos
1. **Registro**: Crea una cuenta con email y contraseña
2. **Login**: Inicia sesión para acceder al dashboard

### ✍️ Gestión de Notas
3. **Crear Nota**: Usa el formulario para crear notas personalizadas
4. **Listar Notas**: Ve todas tus notas en el dashboard
5. **Editar Nota**: Modifica el contenido de notas existentes
6. **Eliminar Nota**: Borra notas que ya no necesites

### 🤖 Funciones de IA
7. **Chat con IA**: Conversa con el asistente para obtener ideas
8. **Generar Contenido**: Crea notas automáticamente desde prompts
9. **Mejorar Notas**: Usa IA para mejorar gramática, estilo o expandir contenido
10. **Resumir Notas**: Obtén resúmenes automáticos de notas largas
11. **Análisis de Notas**: Recibe insights sobre tus patrones de escritura

---

## 📄 Licencia

Este proyecto es una demostración de habilidades de desarrollo Full-Stack para propósitos de portafolio.

## 🤝 Contribuciones

Este es un proyecto de portafolio personal. Si tienes sugerencias o encuentras algún problema, no dudes en abrir un issue.

---

