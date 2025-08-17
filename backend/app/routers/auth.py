from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from app.config import settings
from app.database import get_supabase_admin_client
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

router = APIRouter(tags=["authentication"])

@router.post("/register", response_model=dict)
async def register(user_data: UserCreate):
    """Registrar un nuevo usuario"""
    try:
    
        
        # Generar username si no se proporciona
        if not user_data.username:
            user_data.username = user_data.email.split('@')[0]
    
        
        # Verificar si el usuario ya existe en la tabla users
        existing_user = supabase.table("users").select("*").eq("email", user_data.email).execute()
    
        
        if existing_user.data:
    
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        

        
        # Intentar hacer login para verificar si el usuario existe en Supabase Auth
        try:
    
            test_login = supabase.auth.sign_in_with_password({
                "email": user_data.email,
                "password": user_data.password
            })

            
            if test_login.user:
    
                # El usuario existe en Auth pero no en la tabla users, vamos a sincronizarlo
                user_record = {
                    "id": test_login.user.id,
                    "email": user_data.email,
                    "full_name": user_data.full_name,
                    "username": user_data.username,
                    "password_hash": get_password_hash(user_data.password),
                    "is_active": True
                }
                
                supabase_admin = get_supabase_admin_client()
                result = supabase_admin.table("users").insert(user_record).execute()
                
                if result.data:
                    return {
                        "message": "Usuario registrado exitosamente",
                        "user_id": test_login.user.id
                    }
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Error al sincronizar datos del usuario"
                    )
        except Exception as auth_check_error:
            # Continuar con el proceso normal de registro

            pass
        
        # Crear nuevo usuario en Supabase Auth

        auth_response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })

        
        if not auth_response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al crear usuario en autenticación"
            )
        
        # Insertar datos adicionales en la tabla users usando cliente admin
        hashed_password = get_password_hash(user_data.password)
        
        user_record = {
            "id": auth_response.user.id,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "username": user_data.username,
            "password_hash": hashed_password,
            "is_active": True
        }
        

        # Usar cliente admin para bypasear RLS
        try:
            supabase_admin = get_supabase_admin_client()

            result = supabase_admin.table("users").insert(user_record).execute()

        except Exception as e:

            raise e
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al guardar datos del usuario"
            )
        
        return {
            "message": "Usuario registrado exitosamente",
            "user_id": auth_response.user.id
        }
        
    except HTTPException:
        # Re-lanzar HTTPExceptions sin modificar
        raise
    except Exception as e:
        # Manejar errores específicos de Supabase Auth
        if "User already registered" in str(e) or "already registered" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado. Si crees que esto es un error, contacta al administrador."
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Iniciar sesión"""
    try:
        # Usar el cliente supabase ya configurado
        
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

# Función para obtener el usuario actual
async def get_current_user_dependency(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Obtiene el ID del usuario actual desde el token JWT.
    """
    user_id = get_user_id_from_token(credentials.credentials)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id

@router.get("/me", response_model=User)
async def get_current_user(user_id: str = Depends(get_current_user_dependency)):
    """Obtener información del usuario actual"""
    try:
        # Usar el cliente supabase ya configurado
        
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