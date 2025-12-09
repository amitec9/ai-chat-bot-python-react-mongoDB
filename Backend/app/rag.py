import os
import fitz  # PyMuPDF
from fastapi import APIRouter, UploadFile, File,Request
from fastapi.responses import JSONResponse
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google.generativeai import configure, embed_content
from pinecone import Pinecone, ServerlessSpec

from dotenv import load_dotenv
from .response_manager import ResponseManager
load_dotenv()


router = APIRouter()

# -----------------------------
# 1. Configure Gemini Embeddings
# -----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
configure(api_key=GEMINI_API_KEY)

# -----------------------------
# 2. Configure Pinecone
# -----------------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")

# Create index if not exists
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,       # Gemini text-embedding-004 dimension
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(index_name)

# -----------------------------
# Helper – Extract Text From PDF
# -----------------------------
def extract_text_from_pdf(pdf_bytes: bytes):
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# -----------------------------
# Helper – Generate Embeddings
# -----------------------------
def generate_embedding(text: str):
    response = embed_content(
        model="text-embedding-004",
        content=text
    )
    return response["embedding"]

# -----------------------------
# API: Upload PDF → Chunk → Embed → Upload to Pinecone
# -----------------------------
@router.post("/upload-pdf/")
async def upload_pdf( request: Request,file: UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()
        request_id = request.state.request_id
        # Step 1: Extract Text
        extracted_text = extract_text_from_pdf(pdf_bytes)

        # Step 2: Chunk the text
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_text(extracted_text)

        # Step 3: Embed + Upload to Pinecone
        vectors = []
        for i, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)
            vectors.append({
                "id": f"{file.filename}_chunk_{i}",
                "values": embedding,
                "metadata": {"text": chunk}
            })

        # Upload to Pinecone
        index.upsert(vectors=vectors)
        return ResponseManager.success(
            message="File and db upload successfully",
            result=len(vectors),
            request_id=request_id
        )
        

    except Exception as e:
        return ResponseManager.handle_exception(e, request_id=request.state.request_id)
      
