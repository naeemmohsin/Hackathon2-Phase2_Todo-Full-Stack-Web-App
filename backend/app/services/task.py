"""Task service - business logic for task operations."""

from datetime import datetime
from uuid import UUID
from typing import List, Optional

from sqlmodel import Session, select

from ..models.task import Task


def create_task(db: Session, title: str, owner_id: UUID) -> Task:
    """
    Create a new task for the specified owner.

    Args:
        db: Database session
        title: Task title
        owner_id: UUID of the task owner

    Returns:
        Created Task object
    """
    task = Task(
        title=title,
        owner_id=owner_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session, owner_id: UUID) -> List[Task]:
    """
    Get all tasks for the specified owner.

    Args:
        db: Database session
        owner_id: UUID of the task owner

    Returns:
        List of Task objects belonging to the owner
    """
    statement = select(Task).where(Task.owner_id == owner_id).order_by(Task.created_at.desc())
    return list(db.exec(statement).all())


def get_task_by_id(db: Session, task_id: UUID, owner_id: UUID) -> Optional[Task]:
    """
    Get a specific task by ID, verifying ownership.

    Args:
        db: Database session
        task_id: UUID of the task
        owner_id: UUID of the expected owner

    Returns:
        Task object if found and owned by the user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
    return db.exec(statement).first()


def update_task(db: Session, task_id: UUID, owner_id: UUID, title: str) -> Optional[Task]:
    """
    Update a task's title, verifying ownership.

    Args:
        db: Database session
        task_id: UUID of the task
        owner_id: UUID of the expected owner
        title: New task title

    Returns:
        Updated Task object if found and owned, None otherwise
    """
    task = get_task_by_id(db, task_id, owner_id)
    if not task:
        return None

    task.title = title
    task.updated_at = datetime.utcnow()
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: UUID, owner_id: UUID) -> bool:
    """
    Delete a task, verifying ownership.

    Args:
        db: Database session
        task_id: UUID of the task
        owner_id: UUID of the expected owner

    Returns:
        True if task was deleted, False if not found or not owned
    """
    task = get_task_by_id(db, task_id, owner_id)
    if not task:
        return False

    db.delete(task)
    db.commit()
    return True


def toggle_task(db: Session, task_id: UUID, owner_id: UUID) -> Optional[Task]:
    """
    Toggle a task's completion status, verifying ownership.

    Args:
        db: Database session
        task_id: UUID of the task
        owner_id: UUID of the expected owner

    Returns:
        Updated Task object if found and owned, None otherwise
    """
    task = get_task_by_id(db, task_id, owner_id)
    if not task:
        return None

    task.is_completed = not task.is_completed
    task.updated_at = datetime.utcnow()
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
