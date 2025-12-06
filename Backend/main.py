import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.user import router as user_router
from app.chat_history import router as chat_history
from fastapi import FastAPI,Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
from fastapi.responses import JSONResponse

app = FastAPI(title="AI chat bot API")
# -----------------------------
# ENABLE CORS
# -----------------------------
origins = [ "*",  ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],     # all methods: GET, POST, PUT, DELETE...
    allow_headers=["*"],     # all headers
)
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id  # ✅ Store it here

    response = await call_next(request)

    # Optional: include ID in JSON response
    if response.media_type == "application/json":
        content = b"".join([chunk async for chunk in response.body_iterator])
        import json
        try:
            data = json.loads(content)
            data["request_id"] = request_id
            response = JSONResponse(content=data, status_code=response.status_code)
        except Exception:
            pass

    response.headers["X-Request-ID"] = request_id
    return response

app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(chat_history, prefix="/api/v1/chats", tags=["Save chat history API"])
@app.get("/")
def read_root():
    return {"message": "Welcome to AI chat bot API with MongoDB!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
