from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import uvicorn

# Importar routers
from .routers import auth, notes, gemini
from .config import settings

# Crear la aplicación FastAPI
app = FastAPI(
    title="NOTESIA API",
    description="API para la aplicación de notas inteligentes con IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "https://notesia.vercel.app",  # Dominio de producción
        "*"  # Permitir todos los orígenes temporalmente para debugging
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Manejador de errores de validación
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=400,
        content={
            "detail": "There was an error parsing the body",
            "errors": exc.errors() if settings.debug else None
        }
    )

# Manejador de errores de Pydantic
@app.exception_handler(ValidationError)
async def pydantic_exception_handler(request: Request, exc: ValidationError):

    return JSONResponse(
        status_code=400,
        content={
            "detail": "There was an error parsing the body",
            "errors": exc.errors() if settings.debug else None
        }
    )

# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Error interno del servidor",
            "detail": str(exc) if settings.debug else "Error interno"
        }
    )

# Rutas principales
@app.get("/")
async def root():
    return {
        "message": "¡Bienvenido a NOTESIA API!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai": "ready"
    }

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notas"])
app.include_router(gemini.router, prefix="/api/ai", tags=["Inteligencia Artificial"])

# Para desarrollo local
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
