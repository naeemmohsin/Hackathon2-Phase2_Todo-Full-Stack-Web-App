"""Task-related Pydantic schemas for request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Task title",
    )


class UpdateTaskRequest(BaseModel):
    """Schema for updating a task's title."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Updated task title",
    )


class TaskResponse(BaseModel):
    """Schema for task data in responses."""

    id: UUID
    title: str
    is_completed: bool
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
