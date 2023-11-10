from fastapi import APIRouter
from api.api_v1.endpoints import send_mail_endpoints


api_router = APIRouter()

api_router.include_router(send_mail_endpoints.api_router, prefix='/v1')
