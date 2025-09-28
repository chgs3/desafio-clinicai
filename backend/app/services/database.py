import motor.motor_asyncio
import os
from datetime import datetime
from ..core.agent import TriageState

MONGO_URI = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

db = client.clinicai
interactions_collection = db.get_collection("interactions")
summaries_collection = db.get_collection("summaries")

# função pra salvar interações
async def save_interaction(chat_id: str, sender: str, message: str):
    """Salva uma interação no banco de dados."""
    try:
        await interactions_collection.insert_one({
            "chat_id": chat_id,
            "sender": sender, # ou o usuário ou o agente
            "message": message,
            "timestamp": datetime.utcnow()
        })
    except Exception as e:
        print(f"Erro ao salvar interação: {e}")
        
# função atualizada pra salvar o resumo
async def save_triage_summary(chat_id: str, triage_data: TriageState):
    """Salva o resumo do triagem no banco de dados."""
    try:
        await summaries_collection.update_one(
            {"chat_id": chat_id},
            {"$set": triage_data},
            upsert=True
        )
        print(f"Resumo da traigem salvo com sucesso para o chat_id: {chat_id}")

    except Exception as e:
        print(f"Erro ao salvar resumo da triagem: {e}")