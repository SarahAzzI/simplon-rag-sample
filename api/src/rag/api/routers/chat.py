import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from rag.db.session import get_db
from rag.rag.chat_service import ChatService, ConversationNotFoundError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/conversations", tags=["chat"])

class MessageRequest(BaseModel):
    content: str

@router.post("")
async def create_conversation(db: AsyncSession = Depends(get_db)) -> dict:
    logger.info("Création d'une nouvelle conversation")
    try:
        result = await ChatService().create_conversation(db)
        logger.info("Conversation créée", extra={"conversation_id": str(result.conversation_id)})
        return {"conversation_id": str(result.conversation_id)}
    except Exception as e:
        logger.error("Erreur lors de la création de la conversation", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.post("/{conversation_id}/messages")
async def send_message(
    conversation_id: uuid.UUID,
    body: MessageRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    logger.info("Message reçu", extra={"conversation_id": str(conversation_id)})
    try:
        result = await ChatService().send_message(conversation_id, body.content, db)
        logger.info("Message traité", extra={"message_id": str(result.message_id), "role": result.role})
        return {
            "message_id": str(result.message_id) if result.message_id else None,
            "role": result.role,
            "content": result.content,
            "sources": result.sources,
        }
    except ConversationNotFoundError:
        logger.warning("Conversation introuvable", extra={"conversation_id": str(conversation_id)})
        raise HTTPException(status_code=404, detail="Conversation not found")
    except Exception as e:
        logger.error("Erreur lors de l'envoi du message", extra={"conversation_id": str(conversation_id), "error": str(e)})
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/{conversation_id}/messages")
async def get_messages(
    conversation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    logger.info("Récupération des messages", extra={"conversation_id": str(conversation_id)})
    try:
        items = await ChatService().list_messages(conversation_id, db)
        logger.info("Messages récupérés", extra={"conversation_id": str(conversation_id), "count": len(items)})
        return [
            {
                "message_id": str(item.message_id),
                "role": item.role,
                "content": item.content,
                "sources": item.sources,
                "created_at": item.created_at.isoformat(),
            }
            for item in items
        ]
    except ConversationNotFoundError:
        logger.warning("Conversation introuvable", extra={"conversation_id": str(conversation_id)})
        raise HTTPException(status_code=404, detail="Conversation not found")
    except Exception as e:
        logger.error("Erreur lors de la récupération des messages", extra={"conversation_id": str(conversation_id), "error": str(e)})
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")