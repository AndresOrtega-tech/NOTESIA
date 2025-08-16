from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from datetime import datetime
from supabase import create_client, Client

from app.config import settings
from app.models.note import NoteCreate, NoteUpdate, Note, NoteWithAI, NoteStatus
from app.utils.auth import verify_token, get_user_id_from_token

# Configuración
security = HTTPBearer()

# Cliente Supabase
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)

router = APIRouter(tags=["notes"])

# Función para obtener el usuario actual
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
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

@router.post("/", response_model=Note)
async def create_note(note_data: NoteCreate, user_id: str = Depends(get_current_user)):
    """Crear una nueva nota"""
    try:
        
        note_record = {
            "title": note_data.title,
            "content": note_data.content,
            "user_id": user_id,
            "status": note_data.status.value if note_data.status else NoteStatus.DRAFT.value,
            "tags": note_data.tags or [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        result = supabase.table("notes").insert(note_record).execute()
        
        if result.data:
            return Note(**result.data[0])
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al crear la nota"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )

@router.get("/", response_model=List[Note])
async def get_notes(
    user_id: str = Depends(get_current_user),
    status_filter: Optional[NoteStatus] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0)
):
    """Obtener notas del usuario con filtros opcionales"""
    try:

        
        query = supabase.table("notes").select("*").eq("user_id", user_id)
        
        # Aplicar filtros
        if status_filter:
            query = query.eq("status", status_filter.value)
        
        if search:
            # Buscar en título y contenido
            query = query.or_(f"title.ilike.%{search}%,content.ilike.%{search}%")
        
        # Ordenar por fecha de actualización (más recientes primero)
        query = query.order("updated_at", desc=True)
        
        # Aplicar paginación
        query = query.range(offset, offset + limit - 1)
        
        result = query.execute()
        
        return [Note(**note) for note in result.data]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )

@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: str, user_id: str = Depends(get_current_user)):
    """Obtener una nota específica"""
    try:

        
        result = supabase.table("notes").select("*").eq("id", note_id).eq("user_id", user_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota no encontrada"
            )
        
        return Note(**result.data[0])
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )

@router.put("/{note_id}", response_model=Note)
async def update_note(note_id: str, note_data: NoteUpdate, user_id: str = Depends(get_current_user)):
    """Actualizar una nota"""
    try:

        
        # Verificar que la nota existe y pertenece al usuario
        existing_note = supabase.table("notes").select("*").eq("id", note_id).eq("user_id", user_id).execute()
        
        if not existing_note.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota no encontrada"
            )
        
        # Preparar datos de actualización
        update_data = {"updated_at": datetime.utcnow().isoformat()}
        
        if note_data.title is not None:
            update_data["title"] = note_data.title
        if note_data.content is not None:
            update_data["content"] = note_data.content
        if note_data.status is not None:
            update_data["status"] = note_data.status.value
        if note_data.tags is not None:
            update_data["tags"] = note_data.tags
        
        result = supabase.table("notes").update(update_data).eq("id", note_id).execute()
        
        if result.data:
            return Note(**result.data[0])
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar la nota"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )

@router.delete("/{note_id}")
async def delete_note(note_id: str, user_id: str = Depends(get_current_user)):
    """Eliminar una nota"""
    try:

        
        # Verificar que la nota existe y pertenece al usuario
        existing_note = supabase.table("notes").select("*").eq("id", note_id).eq("user_id", user_id).execute()
        
        if not existing_note.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota no encontrada"
            )
        
        result = supabase.table("notes").delete().eq("id", note_id).execute()
        
        return {"message": "Nota eliminada exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )

@router.get("/tags/list")
async def get_user_tags(user_id: str = Depends(get_current_user)):
    """Obtener todas las etiquetas únicas del usuario"""
    try:

        
        result = supabase.table("notes").select("tags").eq("user_id", user_id).execute()
        
        # Extraer todas las etiquetas únicas
        all_tags = set()
        for note in result.data:
            if note.get("tags"):
                all_tags.update(note["tags"])
        
        return {"tags": sorted(list(all_tags))}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )