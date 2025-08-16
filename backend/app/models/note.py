from optparse import Option
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class NoteStatus (str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

class NoteBase (BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []
    status: NoteStatus = NoteStatus.draft
    
class NoteCreate (NoteBase):
    pass

class NoteUpdate (NoteBase):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[NoteStatus] = None 
    
class NoteInDB (NoteBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class Note (NoteInDB):
    pass

class NoteWithAI (Note):
    ai_suggestion: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_enhanced_content: Optional[str] = None
    ai_suggestions: Optional[List[str]] = []
    generated_content: Optional[str] = None
    analysis: Optional[str] = None
