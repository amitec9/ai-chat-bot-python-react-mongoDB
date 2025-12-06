from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
from .database import conversations_collection, messages_collection

from .response_manager import ResponseManager
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth import decode_access_token  # your JWT decode function
security = HTTPBearer()  # For Authorization header
router = APIRouter()


# -------------------------
# Pydantic Models
# -------------------------
class ConversationModel(BaseModel):
    user_id: str
    title: str
    question: str
    isDeleted: bool = False
    created_at: datetime = datetime.utcnow()


class MessageModel(BaseModel):
    conversation_id: str
    sender: str  # "user" or "assistant"
    message: str
    created_at: datetime = datetime.utcnow()


# -------------------------
# Create Conversation + initial message
# -------------------------
@router.post("/conversation")
async def create_conversation(conversation: ConversationModel, request: Request):
    try:
        request_id = request.state.request_id

        # Save conversation
        conv_data = conversation.dict()
        result = await conversations_collection.insert_one(conv_data)
        conv_id = str(result.inserted_id)

        # Response
        return ResponseManager.success(
            message="Conversation created successfully",
            result={"conversation_id": conv_id},
            request_id=request_id
        )

    except Exception as e:
        return ResponseManager.handle_exception(e, request_id=request.state.request_id)


# -------------------------
# Add message to conversation
# -------------------------
@router.post("/message")
async def add_message(message: MessageModel, request: Request):
    try:
        request_id = request.state.request_id

        # Check if conversation exists
        conv = await conversations_collection.find_one({"_id": ObjectId(message.conversation_id)})
        if not conv:
            return ResponseManager.error(
                message="Conversation not found",
                code=404,
                request_id=request_id
            )

        # Save message
        msg_data = message.dict()
        msg_data["isDeleted"]=False
        msg_data["created_at"] = datetime.utcnow()
        result = await messages_collection.insert_one(msg_data)

        return ResponseManager.success(
            message="Message added successfully",
            result={"message_id": str(result.inserted_id)},
            request_id=request_id
        )

    except Exception as e:
        return ResponseManager.handle_exception(e, request_id=request.state.request_id)


# -------------------------
# Get all messages for a conversation
# -------------------------
@router.get("/{conversation_id}/messages")
async def get_messages(conversation_id: str, request: Request):
    try:
        request_id = request.state.request_id

        messages = []
        async for msg in messages_collection.find({"isDeleted":False,"conversation_id": conversation_id}):
            msg["_id"] = str(msg["_id"])
            msg["created_at"] = msg["created_at"].isoformat()
            messages.append(msg)

        return ResponseManager.success(
            message="Messages fetched successfully",
            result=messages,
            request_id=request_id
        )

    except Exception as e:
        return ResponseManager.handle_exception(e, request_id=request.state.request_id)

# -------------------------
# Soft Delete Conversation + its Messages
# -------------------------
@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str, request: Request):
    try:
        request_id = request.state.request_id

        # Check if conversation exists
        conv = await conversations_collection.find_one({"isDeleted":False,"_id": ObjectId(conversation_id)})
        if not conv:
            return ResponseManager.error(
                message="Conversation not found",
                code=404,
                request_id=request_id
            )

        # Soft delete conversation
        await conversations_collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"isDeleted": True}}
        )

        # Soft delete all related messages
        await messages_collection.update_many(
            {"conversation_id": conversation_id},
            {"$set": {"isDeleted": True}}
        )

        return ResponseManager.success(
            message="Conversation and messages deleted successfully",
            request_id=request_id
        )

    except Exception as e:
        return ResponseManager.handle_exception(e, request_id=request.state.request_id)
    
@router.get("/historylist")
async def get_history(request: Request, token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        request_id = request.state.request_id

        # Decode JWT token to get user_id
        payload = decode_access_token(token.credentials)
        user_id = payload.get("id")
        if not user_id:
            return ResponseManager.error(
                message="Invalid token",
                code=401,
                request_id=request_id
            )

        # Get all conversations of the user
        conversations = []
        async for conv in conversations_collection.find({"user_id": user_id, "isDeleted": False}):
            conv["_id"] = str(conv["_id"])
            conv["created_at"] = conv["created_at"].isoformat()
            conversations.append(conv)

        return ResponseManager.success(
            message="Conversation history fetched successfully",
            result=conversations,
            request_id=request_id
        )

    except Exception as e:
        return ResponseManager.handle_exception(e, request_id=request.state.request_id)