from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from .database import async_session
from .schemas import TodoCreate, TodoUpdate, TodoOut
from .crud import (
    create_todo,
    get_todo,
    update_todo,
    delete_todo,
    list_todos,
)
from .models import StatusEnum

app = FastAPI(
    title="Todo Filter API",
    version="0.2.0",
    description="FastAPI + PostgreSQL で作るフィルタ可能な Todo API",
)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


# ----------------- Health -----------------
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}


# ----------------- CRUD -----------------
@app.post("/todos", response_model=TodoOut, status_code=status.HTTP_201_CREATED, tags=["Todos"])
async def create_todo_endpoint(data: TodoCreate, db: AsyncSession = Depends(get_db)):
    return await create_todo(db, data)


@app.get("/todos/{todo_id}", response_model=TodoOut, tags=["Todos"])
async def read_todo_endpoint(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo = await get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=TodoOut, tags=["Todos"])
async def update_todo_endpoint(todo_id: int, data: TodoUpdate, db: AsyncSession = Depends(get_db)):
    todo = await update_todo(db, todo_id, data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"])
async def delete_todo_endpoint(todo_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_todo(db, todo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Todo not found")
    return


@app.get("/todos", response_model=List[TodoOut], tags=["Todos"])
async def list_todos_endpoint(
    status: Optional[StatusEnum] = Query(None),
    due_before: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    due_after: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    tags: Optional[List[str]] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    order_desc: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    todos, total = await list_todos(
        db,
        status=status,
        due_before=due_before,
        due_after=due_after,
        tags=tags,
        limit=limit,
        offset=offset,
        order_desc=order_desc,
    )

    # ★ Todo → TodoOut に変換して JSON 化
    payload = [
        TodoOut.model_validate(t).model_dump(mode="json") for t in todos
    ]

    from fastapi.responses import JSONResponse

    headers = {"X-Total-Count": str(total)}
    return JSONResponse(content=payload, headers=headers)
