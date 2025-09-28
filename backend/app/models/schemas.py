from pydantic import BaseModel

class ChatRequest(BaseModel):
    chat_id: str
    message: str
    
class ChatResponse(BaseModel):
    response: str