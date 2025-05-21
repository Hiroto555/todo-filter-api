import os
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

# docker-compose.yml の環境変数 DATABASE_URL を優先し、ローカル実行にも対応
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/todo",
)

# 非同期エンジン
engine = create_async_engine(
    DATABASE_URL,
    echo=False,          # SQL ログを見たいときは True
    future=True,
)

# セッションファクトリ（FastAPI 依存性で利用）
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# ベースモデル
Base = declarative_base(metadata=MetaData())
