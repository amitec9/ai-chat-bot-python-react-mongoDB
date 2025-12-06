from fastapi import APIRouter, Request,Depends
from .database import users_collection
from .schemas import UserRegister, UserLogin
from .auth import hash_password, verify_password, create_access_token
from bson import ObjectId
from .response_manager import ResponseManager
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth import decode_access_token  # your JWT decode function
security = HTTPBearer()  # For Authorization header

router = APIRouter()


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "isDeleted": user["isDeleted"],
    }


# ------------------------------
# REGISTER API
# ------------------------------
@router.post("/register")
async def register(user: UserRegister, request: Request):
    try:
        request_id = request.state.request_id

        exist = await users_collection.find_one({"email": user.email})
        if exist:
            return ResponseManager.error(
                message="Email already exists",
                code=400,
                request_id=request_id
            )

        newUser = {
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "password": hash_password(user.password),
            "isDeleted": False,
             "createdAt":  datetime.utcnow()
        }

        result = await users_collection.insert_one(newUser)
        saved_user = await users_collection.find_one({"_id": result.inserted_id})

        return ResponseManager.success(
            message="User registered successfully",
            result=user_helper(saved_user),
            request_id=request_id
        )

    except Exception as e:
        return ResponseManager.handle_exception(e, request_id=request.state.request_id)
    


# ------------------------------
# LOGIN API
# ------------------------------
@router.post("/login")
async def login(user: UserLogin, request: Request):
    try:
        request_id = request.state.request_id

        db_user = await users_collection.find_one({"email": user.email})
        if not db_user:
            return ResponseManager.error(
                message="Invalid email or password",
                code=400,
                request_id=request_id
            )

        if not verify_password(user.password, db_user["password"]):
            return ResponseManager.error(
                message="Invalid email or password",
                code=400,
                request_id=request_id
            )

        token = create_access_token({"id": str(db_user["_id"]), "email": db_user["email"]})
        await users_collection.update_one(
            {"_id": ObjectId(db_user["_id"])},
            {"$set": {"isLogin": True, "lastLoginDate": datetime.utcnow()}}
        )
        return ResponseManager.success(
            message="Login successful",
            result={"token": token},
            request_id=request_id
        )

    except Exception as e:
        return ResponseManager.handle_exception(e, request_id=request.state.request_id)



# ------------------------------
# GET ACTIVE USERS
# ------------------------------
@router.get("/me")
async def get_current_user(request: Request, token: HTTPAuthorizationCredentials = Depends(security)):
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

        user = await users_collection.find_one({"_id": ObjectId(user_id), "isDeleted": False})
        if not user:
            return ResponseManager.error(
                message="User not found",
                code=404,
                request_id=request_id
            )

        return ResponseManager.success(
            message="User fetched successfully",
            result=user_helper(user),
            request_id=request_id
        )

    except Exception as e:
        return ResponseManager.handle_exception(e, request_id=request.state.request_id)



# ------------------------------
# SOFT DELETE USER
# ------------------------------
@router.delete("/users/{id}")
async def delete_user(id: str, request: Request):
    try:
        request_id = request.state.request_id

        result = await users_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"isDeleted": True}}
        )

        if result.modified_count == 0:
            return ResponseManager.error(
                message="User not found",
                code=404,
                request_id=request_id
            )

        return ResponseManager.success(
            message="User deleted successfully",
            request_id=request_id
        )

    except Exception as e:
        return ResponseManager.handle_exception(e, request_id=request.state.request_id)

# ------------------------
# Logout API
# ------------------------
@router.post("/logout")
async def logout(request: Request, token: HTTPAuthorizationCredentials = Depends(security)):
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

        # Set isLogin = False and update lastLoginDate
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"isLogin": False, "lastLoginDate": datetime.utcnow()}}
        )

        return ResponseManager.success(
            message="Logout successful",
            result={"isLogin": False, "lastLoginDate": datetime.utcnow().isoformat()},
            request_id=request_id
        )

    except Exception as e:
        return ResponseManager.handle_exception(e, request_id=request.state.request_id)