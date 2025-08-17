# Guía de Despliegue en Vercel

## Configuración del Proyecto

Este proyecto está configurado para desplegarse en Vercel con:
- **Frontend**: React + Vite
- **Backend**: FastAPI + Python

## Estructura del Proyecto

```
NOTESIA/
├── frontend/          # Aplicación React
│   ├── vercel.json   # Configuración de Vercel para frontend
│   └── ...
├── backend/           # API FastAPI
│   ├── vercel.json   # Configuración de Vercel para backend
│   └── ...
└── DEPLOYMENT.md     # Esta guía
```

## Pasos para Desplegar

### 1. Preparar el Repositorio
```bash
git add .
git commit -m "feat: Ready for Vercel deployment"
git push origin main
```

### 2. Desplegar Backend
1. Ve a [vercel.com](https://vercel.com)
2. Conecta tu repositorio GitHub
3. Crea un nuevo proyecto seleccionando la carpeta `backend`
4. Vercel detectará automáticamente la configuración de Python
5. Despliega el proyecto

### 3. Desplegar Frontend
1. Crea otro proyecto en Vercel
2. Selecciona la carpeta `frontend`
3. Vercel detectará automáticamente la configuración de React
4. Despliega el proyecto

### 4. Configurar Variables de Entorno

#### Backend:
- `DATABASE_URL`: URL de tu base de datos PostgreSQL
- `SECRET_KEY`: Clave secreta para JWT
- `GEMINI_API_KEY`: Clave de API de Google Gemini

#### Frontend:
- No requiere variables adicionales (usa la configuración automática)

## URLs de Producción

- **Backend**: `https://notesia.vercel.app/api`
- **Frontend**: Se configurará automáticamente al desplegar

## Verificación del Despliegue

1. Verifica que el backend responda: `https://notesia.vercel.app/api/health`
2. Verifica que el frontend cargue correctamente
3. Prueba el registro y login de usuarios
4. Prueba la creación, edición y eliminación de notas

## Notas Importantes

- El frontend está configurado para usar automáticamente la URL de producción en Vercel
- Asegúrate de que las variables de entorno estén configuradas correctamente
- El backend usa PostgreSQL como base de datos en producción