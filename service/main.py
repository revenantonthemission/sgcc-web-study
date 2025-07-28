import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import FastAPI, HTTPException, Depends, status, Request, Query
from pydantic import BaseModel, Field
from typing import List, AsyncGenerator
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# --- 기본 설정 ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 데이터베이스 설정 ---
DATABASE_URL = "mysql+aiomysql://root:phoenix@localhost:3306/memo_app"

metadata = sqlalchemy.MetaData()
memos = sqlalchemy.Table(
    "memos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("title", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()),
)

# --- 애플리케이션 생명주기 및 리소스 초기화 ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Lifespan: 애플리케이션 시작...")
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
    app.state.db_engine = engine
    app.state.db_session_factory = async_session_factory
    logger.info("Lifespan: 데이터베이스 리소스가 app.state에 저장되었습니다.")

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    logger.info("Lifespan: 데이터베이스 테이블이 성공적으로 준비되었습니다.")

    yield

    logger.info("Lifespan: 애플리케이션 종료...")
    await app.state.db_engine.dispose()
    logger.info("Lifespan: 데이터베이스 연결이 성공적으로 해제되었습니다.")


# --- FastAPI 앱 인스턴스 생성 및 lifespan 연결 ---
app = FastAPI(
    title="Memo API",
    description="FastAPI, SQLAlchemy 2.0, Asyncio를 사용한 비동기 메모 애플리케이션",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic 스키마 정의 ---
class MemoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="메모 제목")
    content: str = Field(..., min_length=1, description="메모 내용")

class MemoCreate(MemoBase):
    pass

class MemoUpdate(BaseModel):
    title: str = Field(None, min_length=1, max_length=100, description="메모 제목 (선택 사항)")
    content: str = Field(None, min_length=1, description="메모 내용 (선택 사항)")

class MemoInDB(MemoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# --- 데이터베이스 의존성 주입 ---
async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session_factory = request.app.state.db_session_factory
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


# --- API 엔드포인트 ---

@app.post("/memos/", response_model=MemoInDB, status_code=status.HTTP_201_CREATED, summary="새 메모 생성")
async def create_memo(memo: MemoCreate, db: AsyncSession = Depends(get_db)):
    try:
        query = memos.insert().values(title=memo.title, content=memo.content)
        result = await db.execute(query)
        await db.commit()
        
        created_id = result.lastrowid
        created_memo_query = memos.select().where(memos.c.id == created_id)
        created_memo = await db.execute(created_memo_query)
        
        return created_memo.mappings().one()
    except Exception as e:
        await db.rollback()
        logger.error(f"메모 생성 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="메모 생성에 실패했습니다.")


@app.get("/memos/", response_model=List[MemoInDB], summary="모든 메모 조회")
async def read_memos(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    try:
        query = memos.select().order_by(memos.c.id.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error(f"메모 목록 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="메모를 불러오는 데 실패했습니다.")


@app.get("/memos/{memo_id}", response_model=MemoInDB, summary="특정 메모 조회")
async def read_memo(memo_id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = memos.select().where(memos.c.id == memo_id)
        result = await db.execute(query)
        memo = result.mappings().first()
        if memo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {memo_id}에 해당하는 메모를 찾을 수 없습니다.")
        return memo
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"메모(ID:{memo_id}) 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="메모 조회 중 오류가 발생했습니다.")


@app.put("/memos/{memo_id}", response_model=MemoInDB, summary="특정 메모 수정")
async def update_memo(memo_id: int, memo: MemoUpdate, db: AsyncSession = Depends(get_db)):
    try:
        existing_memo_query = memos.select().where(memos.c.id == memo_id)
        existing_memo = (await db.execute(existing_memo_query)).mappings().first()
        if existing_memo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {memo_id}에 해당하는 메모를 찾을 수 없습니다.")

        update_data = memo.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정할 내용이 없습니다.")

        query = memos.update().where(memos.c.id == memo_id).values(**update_data)
        await db.execute(query)
        await db.commit()

        updated_memo_query = memos.select().where(memos.c.id == memo_id)
        updated_memo = (await db.execute(updated_memo_query)).mappings().one()
        return updated_memo
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"메모(ID:{memo_id}) 수정 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="메모 수정 중 오류가 발생했습니다.")


@app.delete("/memos/{memo_id}", status_code=status.HTTP_204_NO_CONTENT, summary="특정 메모 삭제")
async def delete_memo(memo_id: int, db: AsyncSession = Depends(get_db)):
    try:
        existing_memo_query = memos.select().where(memos.c.id == memo_id)
        existing_memo = (await db.execute(existing_memo_query)).mappings().first()
        if existing_memo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {memo_id}에 해당하는 메모를 찾을 수 없습니다.")

        delete_query = memos.delete().where(memos.c.id == memo_id)
        await db.execute(delete_query)
        await db.commit()
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"메모(ID:{memo_id}) 삭제 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="메모 삭제 중 오류가 발생했습니다.")


@app.get("/memos/search/", response_model=List[MemoInDB], summary="메모 검색")
async def search_memos(q: str = Query(..., min_length=1, description="검색어"), db: AsyncSession = Depends(get_db)):
    try:
        search_query = f"%{q}%"
        query = memos.select().where(
            sqlalchemy.or_(
                memos.c.title.like(search_query),
                memos.c.content.like(search_query)
            )
        ).order_by(memos.c.id.desc())
        
        result = await db.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error(f"메모 검색 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="메모 검색 중 오류가 발생했습니다.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
