from fastapi import APIRouter, HTTPException
from ..models import schemas
from ..core import agent
from ..services import database

router = APIRouter()

@router.post("/chat", response_model=schemas.ChatResponse)
async def handle_chat(request: schemas.ChatRequest):
    """ Endpoint para processar mensagens de chat. """
    try:
        agent_result = await agent.run_agent_turn(request.chat_id, request.message)
        agent_response = agent_result["response"]
        
        # Salva a interação no banco de dados
        await database.save_interaction(request.chat_id, "user", request.message)
        await database.save_interaction(request.chat_id, "agent", agent_response)
        
        # se o agente finalizou a triagem, salva o resumo
        if agent_result["is_complete"]:
            await database.save_triage_summary(request.chat_id, agent_result["state"])
            
        return schemas.ChatResponse(response=agent_response)
    
    except Exception as e:
        print(f"Erro ao processar o /chat: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")