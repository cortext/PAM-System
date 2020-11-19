from fastapi import APIRouter

from pam.api.api_v1.endpoints import entities

api_router = APIRouter()
api_router.include_router(entities.router)
