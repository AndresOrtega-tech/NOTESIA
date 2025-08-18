from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from typing import Optional
import google.generativeai as genai
from pydantic import BaseModel
from supabase import create_client, Client

from app.config import settings
from app.models.note import Note, NoteWithAI
from app.routers.auth import get_current_user_dependency

# Configuración
security = HTTPBearer()

# Cliente Supabase
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)

# Configurar Gemini AI
genai.configure(api_key=settings.gemini_api_key)

router = APIRouter(tags=["ai"])

# Usar la dependencia de autenticación centralizada
get_current_user = get_current_user_dependency

# Modelos para las peticiones de IA
class AIPrompt(BaseModel):
    prompt: str
    context: Optional[str] = None

class SummarizeRequest(BaseModel):
    note_id: str

class EnhanceRequest(BaseModel):
    note_id: str
    enhancement_type: str = "improve"  # improve, expand, simplify

class GenerateFromPrompt(BaseModel):
    prompt: str
    title: Optional[str] = None

@router.post("/chat")
async def chat_with_ai(ai_prompt: AIPrompt, user_id: str = Depends(get_current_user)):
    """Chat general con IA especializado en tomar notas"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt del sistema para definir el rol del asistente
        system_prompt = """Eres un asistente especializado en tomar notas y organizar información. Tu función principal es ayudar a los usuarios a:

1. Resumir textos largos en puntos clave y conceptos principales
2. Generar ideas y estructurar información de manera clara
3. Extraer información importante y relevante de textos
4. Organizar y estructurar notas de forma eficiente
5. Ayudar a pensar en ideas y conceptos relacionados

Siempre proporciona respuestas claras, bien estructuradas y enfocadas en la productividad y organización de información. Usa formato markdown cuando sea apropiado para mejorar la legibilidad."""
        
        # Construir el prompt completo
        if ai_prompt.context:
            full_prompt = f"{system_prompt}\n\nContexto: {ai_prompt.context}\n\nPregunta del usuario: {ai_prompt.prompt}"
        else:
            full_prompt = f"{system_prompt}\n\nPregunta del usuario: {ai_prompt.prompt}"
        
        response = model.generate_content(full_prompt)
        
        return {
            "response": response.text,
            "prompt": ai_prompt.prompt
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar con IA: {str(e)}"
        )

@router.post("/summarize", response_model=NoteWithAI)
async def summarize_note(request: SummarizeRequest, user_id: str = Depends(get_current_user)):
    """Generar resumen de una nota"""
    try:

        
        # Obtener la nota
        result = supabase.table("notes").select("*").eq("id", request.note_id).eq("user_id", user_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota no encontrada"
            )
        
        note_data = result.data[0]
        note = Note(**note_data)
        
        # Generar resumen con IA
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Por favor, genera un resumen conciso y útil del siguiente contenido:
        
        Título: {note.title}
        Contenido: {note.content}
        
        El resumen debe:
        - Capturar los puntos principales
        - Ser claro y conciso
        - Mantener la información más importante
        - Tener máximo 3-4 oraciones
        """
        
        response = model.generate_content(prompt)
        
        return NoteWithAI(
            **note.dict(),
            ai_summary=response.text,
            ai_suggestions=[]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar resumen: {str(e)}"
        )

@router.post("/enhance", response_model=NoteWithAI)
async def enhance_note(request: EnhanceRequest, user_id: str = Depends(get_current_user)):
    """Mejorar una nota con IA"""
    try:

        
        # Obtener la nota
        result = supabase.table("notes").select("*").eq("id", request.note_id).eq("user_id", user_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota no encontrada"
            )
        
        note_data = result.data[0]
        note = Note(**note_data)
        
        # Definir prompts según el tipo de mejora
        enhancement_prompts = {
            "improve": "Mejora la claridad, estructura y gramática del siguiente texto, manteniendo el significado original:",
            "expand": "Expande el siguiente contenido añadiendo más detalles, ejemplos y explicaciones relevantes:",
            "simplify": "Simplifica el siguiente texto haciéndolo más fácil de entender, manteniendo la información esencial:"
        }
        
        prompt_base = enhancement_prompts.get(request.enhancement_type, enhancement_prompts["improve"])
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""{prompt_base}
        
        Título: {note.title}
        Contenido: {note.content}
        
        Proporciona el contenido mejorado manteniendo el formato y estructura apropiados.
        """
        
        response = model.generate_content(prompt)
        
        # Generar sugerencias adicionales
        suggestions_prompt = f"""Basándote en el siguiente contenido, proporciona 3-5 sugerencias breves para mejorarlo aún más:
        
        {note.content}
        
        Las sugerencias deben ser específicas y accionables.
        """
        
        suggestions_response = model.generate_content(suggestions_prompt)
        suggestions = [s.strip() for s in suggestions_response.text.split('\n') if s.strip() and not s.strip().startswith('#')]
        
        return NoteWithAI(
            **note.dict(),
            ai_enhanced_content=response.text,
            ai_suggestions=suggestions[:5]  # Limitar a 5 sugerencias
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al mejorar nota: {str(e)}"
        )

@router.post("/generate", response_model=dict)
async def generate_note_from_prompt(request: GenerateFromPrompt, user_id: str = Depends(get_current_user)):
    """Generar contenido de nota desde un prompt"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""Genera contenido para una nota basándote en la siguiente solicitud:
        
        {request.prompt}
        
        El contenido debe ser:
        - Bien estructurado y organizado
        - Informativo y útil
        - Apropiado para una aplicación de notas
        - Incluir puntos principales y detalles relevantes
        
        Si no se proporciona un título específico, sugiere uno apropiado.
        """
        
        response = model.generate_content(prompt)
        
        # Generar título si no se proporciona
        title = request.title
        if not title:
            title_prompt = f"Genera un título conciso y descriptivo para el siguiente contenido:\n\n{response.text[:200]}..."
            title_response = model.generate_content(title_prompt)
            title = title_response.text.strip().replace('"', '').replace('Título:', '').strip()
        
        return {
            "title": title,
            "content": response.text,
            "generated_from_prompt": request.prompt
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar contenido: {str(e)}"
        )

@router.post("/analyze-notes")
async def analyze_user_notes(user_id: str = Depends(get_current_user)):
    """Analizar todas las notas del usuario y proporcionar insights"""
    try:

        
        # Obtener todas las notas del usuario
        result = supabase.table("notes").select("title, content, tags, created_at").eq("user_id", user_id).execute()
        
        if not result.data:
            return {
                "message": "No hay notas para analizar",
                "insights": []
            }
        
        # Preparar contenido para análisis
        notes_summary = "\n\n".join([
            f"Título: {note['title']}\nContenido: {note['content'][:200]}..."
            for note in result.data[:10]  # Limitar a 10 notas para evitar tokens excesivos
        ])
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Analiza las siguientes notas de un usuario y proporciona insights útiles:
        
        {notes_summary}
        
        Proporciona:
        1. Temas principales identificados
        2. Patrones en el contenido
        3. Sugerencias para organización
        4. Áreas de interés del usuario
        5. Recomendaciones para mejorar la productividad
        
        Mantén el análisis conciso y accionable.
        """
        
        response = model.generate_content(prompt)
        
        return {
            "total_notes_analyzed": len(result.data),
            "insights": response.text,
            "analysis_date": "2024-01-01"  # Usar fecha actual en implementación real
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al analizar notas: {str(e)}"
        )