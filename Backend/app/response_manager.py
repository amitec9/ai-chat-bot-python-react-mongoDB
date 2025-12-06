# Commen Response  file
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import traceback

class ResponseManager:
    @staticmethod
    def success(message: str = "Success", result=None,request_id: str = None, code: int = 200,):
        """✅ Uniform success response"""
        return JSONResponse(
            status_code=code,
            content={
                "success":True,
                "code": code,
                "message": message,
                "result": result,
                "request_id":request_id
            }

        )

    @staticmethod
    def error(message: str = "Something went wrong", error=None, code: int = 400,request_id: str = None):
        """❌ Uniform error response"""
        return JSONResponse(
            status_code=code,
            content={
                "success":False,
                "code": code,
                "message": message,
                "request_id":request_id,
                "error": str(error)
            }
        )

    @staticmethod
    def handle_exception(e: Exception, request_id: str = None, message: str = "Internal Server Error"):
        """🔥 Unified exception handler"""
        # ✅ Return standardized error response
        return JSONResponse(
            content={
                "success": False,
                "message": message,
                "error": str(e),
                "request_id": request_id
            },
            status_code=400
        )

