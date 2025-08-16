from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from app.config import settings
from app.models.user import UserCreate, UserResponse, UserLogin, Token, User
from app.utils.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    get_user_id_from_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Configuración
security = HTTPBearer()

# Cliente Supabase
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=dict)
async def register(user_data: UserCreate):
    """Registrar un nuevo usuario"""
    try:
        supabase = get_supabase_client()
        
        # Verificar si el usuario ya existe
        existing_user = supabase.table("users").select("*").eq("email", user_data.email).execute()
        if existing_user.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe"
            )
        
        # Crear nuevo usuario en Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })
        
        if auth_response.user:
            # Insertar datos adicionales en la tabla users
            user_record = {
                "id": auth_response.user.id,
                "email": user_data.email,
                "full_name": user_data.full_name,
                "is_active": True
            }
            
            result = supabase.table("users").insert(user_record).execute()
            
            return {
                "message": "Usuario registrado exitosamente",
                "user_id": auth_response.user.id
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al crear usuario"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Iniciar sesión"""
    try:
        supabase = get_supabase_client()
        
        # Autenticar con Supabase
        auth_response = supabase.auth.sign_in_with_password({
            "email": user_credentials.email,
            "password": user_credentials.password
        })
        
        if auth_response.user:
            # Crear token JWT personalizado
            access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
            access_token = create_access_token(
                data={"sub": auth_response.user.id},
                expires_delta=access_token_expires
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": settings.access_token_expire_minutes * 60
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

@router.get("/me", response_model=User)
async def get_current_user(user_id: str = Depends(verify_token)):
    """Obtener información del usuario actual"""
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("users").select("*").eq("id", user_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        user_data = result.data[0]
        return User(**user_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )

@router.post("/logout")
async def logout():
    """Cerrar sesión (invalidar token)"""
    # En una implementación real, podrías mantener una lista negra de tokens
    return {"message": "Sesión cerrada exitosamente"}