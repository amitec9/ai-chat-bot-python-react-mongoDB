from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)

db = client["mydatabase"]   # your DB name
users_collection = db["users"]
conversations_collection = db["conversations"]
messages_collection = db["messages"]
