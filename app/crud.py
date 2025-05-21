from typing import List, Optional, Tuple

from sqlalchemy import select, update, delete, func, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Todo, StatusEnum
from .schemas import TodoCreate, TodoUpdate


# ------------- 作成 -------------
async def create_todo(db: AsyncSession, data: TodoCreate) -> Todo:
    todo = Todo(**data.model_dump())
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


# ------------- 取得（単体） -------------
async def get_todo(db: AsyncSession, todo_id: int) -> Optional[Todo]:
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    return result.scalar_one_or_none()


# ------------- 更新 -------------
async def update_todo(db: AsyncSession, todo_id: int, data: TodoUpdate) -> Optional[Todo]:
    result = await db.execute(
        update(Todo)
        .where(Todo.id == todo_id)
        .values(**data.model_dump(exclude_none=True))
        .returning(Todo)
    )
    todo = result.scalar_one_or_none()
    if todo:
        await db.commit()
    return todo


# ------------- 削除 -------------
async def delete_todo(db: AsyncSession, todo_id: int) -> bool:
    result = await db.execute(
        delete(Todo)
        .where(Todo.id == todo_id)
        .returning(Todo.id)
    )
    todo_id_row = result.scalar_one_or_none()
    if todo_id_row:
        await db.commit()
        return True
    return False


# ------------- 検索 with 絞り込み & ページネーション -------------
async def list_todos(
    db: AsyncSession,
    *,
    status: Optional[StatusEnum] = None,
    due_before: Optional[str] = None,
    due_after: Optional[str] = None,
    tags: Optional[List[str]] = None,
    limit: int = 20,
    offset: int = 0,
    order_desc: bool = False,
) -> Tuple[List[Todo], int]:
    stmt = select(Todo)

    if status:
        stmt = stmt.where(Todo.status == status)
    if due_before:
        stmt = stmt.where(Todo.due_date <= due_before)
    if due_after:
        stmt = stmt.where(Todo.due_date >= due_after)
    if tags:
        stmt = stmt.where(Todo.tags.op("@>")(tags))  # 全タグ含む

    total = await db.scalar(select(func.count()).select_from(stmt.subquery()))

    order_clause = desc(Todo.id) if order_desc else asc(Todo.id)
    stmt = stmt.order_by(order_clause).limit(limit).offset(offset)

    result = await db.execute(stmt)
    return result.scalars().all(), total

