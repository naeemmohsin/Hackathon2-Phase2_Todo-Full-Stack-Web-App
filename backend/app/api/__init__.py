"""API routes package - aggregates all routers."""

from fastapi import APIRouter

from .auth import router as auth_router

# Main API router that includes all sub-routers
api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth")

__all__ = ["api_router", "auth_router"]
