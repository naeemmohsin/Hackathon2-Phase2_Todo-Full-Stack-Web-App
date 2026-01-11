"""Task management API endpoints."""

from uuid import UUID
from typing import List

from fastapi import APIRouter, HTTPException, status

from ..api.deps import DbSession, CurrentUser
from ..schemas.task import CreateTaskRequest, UpdateTaskRequest, TaskResponse
from ..services.task import create_task, list_tasks, update_task, delete_task, toggle_task

router = APIRouter(tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
def get_all_tasks(
    db: DbSession,
    current_user: CurrentUser,
) -> List[TaskResponse]:
    """
    Get all tasks for the authenticated user.

    - Returns tasks ordered by creation date (newest first)
    - Only returns tasks owned by the current user
    """
    tasks = list_tasks(db=db, owner_id=current_user.id)
    return [
        TaskResponse(
            id=task.id,
            title=task.title,
            is_completed=task.is_completed,
            owner_id=task.owner_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        for task in tasks
    ]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    request: CreateTaskRequest,
    db: DbSession,
    current_user: CurrentUser,
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    - Title is required and must be 1-500 characters
    - Task is automatically assigned to the current user
    """
    task = create_task(
        db=db,
        title=request.title,
        owner_id=current_user.id,
    )

    return TaskResponse(
        id=task.id,
        title=task.title,
        is_completed=task.is_completed,
        owner_id=task.owner_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_title(
    task_id: UUID,
    request: UpdateTaskRequest,
    db: DbSession,
    current_user: CurrentUser,
) -> TaskResponse:
    """
    Update a task's title.

    - Only the task owner can update the task
    - Returns 404 if task doesn't exist or is not owned by the user
    """
    task = update_task(
        db=db,
        task_id=task_id,
        owner_id=current_user.id,
        title=request.title,
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied",
        )

    return TaskResponse(
        id=task.id,
        title=task.title,
        is_completed=task.is_completed,
        owner_id=task.owner_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_by_id(
    task_id: UUID,
    db: DbSession,
    current_user: CurrentUser,
) -> None:
    """
    Delete a task.

    - Only the task owner can delete the task
    - Returns 404 if task doesn't exist or is not owned by the user
    """
    success = delete_task(
        db=db,
        task_id=task_id,
        owner_id=current_user.id,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied",
        )


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
def toggle_task_completion(
    task_id: UUID,
    db: DbSession,
    current_user: CurrentUser,
) -> TaskResponse:
    """
    Toggle a task's completion status.

    - Only the task owner can toggle the task
    - Returns 404 if task doesn't exist or is not owned by the user
    """
    task = toggle_task(
        db=db,
        task_id=task_id,
        owner_id=current_user.id,
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied",
        )

    return TaskResponse(
        id=task.id,
        title=task.title,
        is_completed=task.is_completed,
        owner_id=task.owner_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
