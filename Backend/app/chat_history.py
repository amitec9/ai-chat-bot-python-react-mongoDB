from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
from .database import conversations_collection, messages_collection

from .response_manager import ResponseManager
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from .auth import decode_access_token  # your JWT decode function
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY:", GEMINI_API_KEY)

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)
security = HTTPBearer()  # For Authorization header
router = APIRouter()
from typing import List, Dict

# -------------------------
# Pydantic Models
# -------------------------
class ConversationModel(BaseModel):
    title: str
    question: str


class MessageModel(BaseModel):
    conversation_id: str
    sender: str  # "user" or "assistant"
    message: str
    created_at: datetime = datetime.utcnow()


# -------------------------
# Create Conversation + initial message
# -------------------------
@router.post("/conversation")
async def create_conversation(conversation: ConversationModel, request: Request,token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        request_id = request.state.request_id
        payload = decode_access_token(token.credentials)
        user_id = payload.get("id")
        if not user_id:
            return ResponseManager.error(
                message="Invalid token",
                code=401,
                request_id=request_id
            )
        # Save conversation
        conv_data = conversation.dict()
        conv_data["user_id"]=user_id
        conv_data["isDeleted"]=False
        conv_data["created_at"] = datetime.utcnow()
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
History: List[Dict] = []
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
          # Add user message to history
        History.append({"role": "user", "parts": [{"text": message.message}]})

        # Call Gemini API
        response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=History,
        config={
            "system_instruction": """
        You are a JavaScript  Instructor. You will only reply to the problem related to 
        JavaScript . You have to solve query of user in simplest way
        If user ask any question which is not related to JavaScript , reply him rudely
        Example: If user ask, How are you
            You will reply: You dumb ask me some sensible question, like this message you can reply anything more rudely
            
            You have to reply him rudely if question is not related to JavaScript.
            Else reply him politely with simple explanation.
            """
        }
    )

    

        # Add AI response to history
        ai_reply = response.text
        History.append({"role": "model", "parts": [{"text": response.text}]})

        
        # Save message
          # ---------------------------
        # Save USER message in MongoDB
        # ---------------------------
        user_msg = {
            "conversation_id": message.conversation_id,
            "sender": "user",
            "message": message.message,
            "isDeleted": False,
            "created_at": datetime.utcnow()
        }
        await messages_collection.insert_one(user_msg)

        # ---------------------------
        # Save ASSISTANT message
        # ---------------------------
        assistant_msg = {
            "conversation_id": message.conversation_id,
            "sender": "assistant",
            "message": ai_reply,
            "isDeleted": False,
            "created_at": datetime.utcnow()
        }
        result = await messages_collection.insert_one(assistant_msg)


        return ResponseManager.success(
            message="Message added successfully",
            result={"message_id": str(result.inserted_id)},
            request_id=request_id
        )

    except Exception as e:
        print(e)
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