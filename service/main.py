import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import FastAPI, HTTPException, Depends, status, Request, Query
from pydantic import BaseModel, Field
from typing import List, AsyncGenerator, Optional
from datetime import datetime, date
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# --- 기본 설정 ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 데이터베이스 설정 ---
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+aiomysql://memo_user:phoenix@localhost:3306/memo_app"
)

metadata = sqlalchemy.MetaData()
memos = sqlalchemy.Table(
    "memos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("title", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("tags", sqlalchemy.JSON, nullable=True, default=[]),
    sqlalchemy.Column("priority", sqlalchemy.Integer, nullable=False, default=2, server_default="2"),
    sqlalchemy.Column("category", sqlalchemy.String(50), nullable=True),
    sqlalchemy.Column("is_archived", sqlalchemy.Boolean, nullable=False, default=False, server_default="0"),
    sqlalchemy.Column("is_favorite", sqlalchemy.Boolean, nullable=False, default=False, server_default="0"),
    sqlalchemy.Column("author", sqlalchemy.String(100), nullable=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()),
)

# --- 애플리케이션 생명주기 및 리소스 초기화 ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Lifespan: 애플리케이션 시작...")
    engine = create_async_engine(
        DATABASE_URL, 
        echo=True,
        pool_size=10,
        max_overflow=20,
        pool_timeout=30,
        pool_recycle=3600,
        pool_pre_ping=True
    )
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
    tags: Optional[List[str]] = Field(default=[], description="태그 목록")
    priority: int = Field(default=2, ge=1, le=4, description="우선순위 (1:낮음, 2:보통, 3:높음, 4:긴급)")
    category: Optional[str] = Field(None, max_length=50, description="카테고리")
    is_archived: bool = Field(default=False, description="아카이브 여부")
    is_favorite: bool = Field(default=False, description="즐겨찾기 여부")
    author: Optional[str] = Field(None, max_length=100, description="작성자")

class MemoCreate(MemoBase):
    pass

class MemoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="메모 제목 (선택 사항)")
    content: Optional[str] = Field(None, min_length=1, description="메모 내용 (선택 사항)")
    tags: Optional[List[str]] = Field(None, description="태그 목록 (선택 사항)")
    priority: Optional[int] = Field(None, ge=1, le=4, description="우선순위 (선택 사항)")
    category: Optional[str] = Field(None, max_length=50, description="카테고리 (선택 사항)")
    is_archived: Optional[bool] = Field(None, description="아카이브 여부 (선택 사항)")
    is_favorite: Optional[bool] = Field(None, description="즐겨찾기 여부 (선택 사항)")
    author: Optional[str] = Field(None, max_length=100, description="작성자 (선택 사항)")

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
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# --- API 엔드포인트 ---

@app.post("/memos/", response_model=MemoInDB, status_code=status.HTTP_201_CREATED, summary="새 메모 생성")
async def create_memo(memo: MemoCreate, db: AsyncSession = Depends(get_db)):
    try:
        query = memos.insert().values(
            title=memo.title,
            content=memo.content,
            tags=memo.tags or [],
            priority=memo.priority,
            category=memo.category,
            is_archived=memo.is_archived,
            is_favorite=memo.is_favorite,
            author=memo.author
        )
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


@app.get("/memos/list-by-date/", response_model=List[MemoInDB], summary="날짜 범위로 메모 조회")
async def list_memos_by_date(
    start_date: Optional[date] = Query(None, description="시작 날짜 (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="종료 날짜 (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(100, ge=1, le=1000, description="반환할 최대 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = memos.select()
        
        if start_date:
            query = query.where(memos.c.created_at >= start_date)
        if end_date:
            query = query.where(memos.c.created_at < sqlalchemy.func.date_add(end_date, sqlalchemy.text("INTERVAL 1 DAY")))
            
        query = query.order_by(memos.c.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error(f"날짜별 메모 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="날짜별 메모 조회 중 오류가 발생했습니다.")


@app.get("/memos/list-by-title-prefix/", response_model=List[MemoInDB], summary="제목 접두사로 메모 조회")
async def list_memos_by_title_prefix(
    prefix: str = Query(..., min_length=1, description="제목 접두사"),
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(100, ge=1, le=1000, description="반환할 최대 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    try:
        search_pattern = f"{prefix}%"
        query = memos.select().where(
            memos.c.title.like(search_pattern)
        ).order_by(memos.c.title).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error(f"제목 접두사별 메모 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="제목 접두사별 메모 조회 중 오류가 발생했습니다.")


@app.get("/memos/list-recent/", response_model=List[MemoInDB], summary="최근 활동 메모 조회")
async def list_recent_memos(
    days: int = Query(7, ge=1, le=365, description="최근 N일 이내"),
    order_by: str = Query("updated", description="정렬 기준 (created|updated)"),
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(100, ge=1, le=1000, description="반환할 최대 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    try:
        cutoff_date = sqlalchemy.func.date_sub(sqlalchemy.func.now(), sqlalchemy.text(f"INTERVAL {days} DAY"))
        
        if order_by == "created":
            query = memos.select().where(
                memos.c.created_at >= cutoff_date
            ).order_by(memos.c.created_at.desc())
        else:
            query = memos.select().where(
                memos.c.updated_at >= cutoff_date
            ).order_by(memos.c.updated_at.desc())
            
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error(f"최근 메모 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="최근 메모 조회 중 오류가 발생했습니다.")


@app.get("/memos/list-by-keywords/", response_model=List[MemoInDB], summary="키워드로 메모 조회")
async def list_memos_by_keywords(
    keywords: str = Query(..., min_length=1, description="공백으로 구분된 키워드들"),
    match_all: bool = Query(False, description="모든 키워드 포함 여부 (기본값: 하나라도 포함)"),
    search_in: str = Query("both", description="검색 대상 (title|content|both)"),
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(100, ge=1, le=1000, description="반환할 최대 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    try:
        keyword_list = [kw.strip() for kw in keywords.split() if kw.strip()]
        if not keyword_list:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="최소 하나의 키워드가 필요합니다.")
        
        conditions = []
        for keyword in keyword_list:
            search_pattern = f"%{keyword}%"
            keyword_conditions = []
            
            if search_in in ["title", "both"]:
                keyword_conditions.append(memos.c.title.like(search_pattern))
            if search_in in ["content", "both"]:
                keyword_conditions.append(memos.c.content.like(search_pattern))
                
            conditions.append(sqlalchemy.or_(*keyword_conditions))
        
        if match_all:
            final_condition = sqlalchemy.and_(*conditions)
        else:
            final_condition = sqlalchemy.or_(*conditions)
            
        query = memos.select().where(final_condition).order_by(memos.c.updated_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.mappings().all()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"키워드별 메모 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="키워드별 메모 조회 중 오류가 발생했습니다.")


@app.get("/memos/list-by-priority/", response_model=List[MemoInDB], summary="우선순위별 메모 조회")
async def list_memos_by_priority(
    priority: int = Query(..., ge=1, le=4, description="우선순위 (1:낮음, 2:보통, 3:높음, 4:긴급)"),
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(100, ge=1, le=1000, description="반환할 최대 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = memos.select().where(
            memos.c.priority == priority
        ).order_by(memos.c.updated_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error(f"우선순위별 메모 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="우선순위별 메모 조회 중 오류가 발생했습니다.")


@app.get("/memos/list-by-category/", response_model=List[MemoInDB], summary="카테고리별 메모 조회")
async def list_memos_by_category(
    category: str = Query(..., min_length=1, description="카테고리"),
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(100, ge=1, le=1000, description="반환할 최대 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = memos.select().where(
            memos.c.category == category
        ).order_by(memos.c.updated_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error(f"카테고리별 메모 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="카테고리별 메모 조회 중 오류가 발생했습니다.")


@app.get("/memos/list-by-tags/", response_model=List[MemoInDB], summary="태그별 메모 조회")
async def list_memos_by_tags(
    tags: str = Query(..., min_length=1, description="콤마로 구분된 태그 목록"),
    match_all: bool = Query(False, description="모든 태그 포함 여부 (기본값: 하나라도 포함)"),
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(100, ge=1, le=1000, description="반환할 최대 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    try:
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        if not tag_list:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="최소 하나의 태그가 필요합니다.")
        
        if match_all:
            conditions = [sqlalchemy.func.json_contains(memos.c.tags, f'"{tag}"') for tag in tag_list]
            final_condition = sqlalchemy.and_(*conditions)
        else:
            conditions = [sqlalchemy.func.json_contains(memos.c.tags, f'"{tag}"') for tag in tag_list]
            final_condition = sqlalchemy.or_(*conditions)
            
        query = memos.select().where(final_condition).order_by(memos.c.updated_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.mappings().all()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"태그별 메모 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="태그별 메모 조회 중 오류가 발생했습니다.")


@app.get("/memos/list-archived/", response_model=List[MemoInDB], summary="아카이브된 메모 조회")
async def list_archived_memos(
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(100, ge=1, le=1000, description="반환할 최대 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = memos.select().where(
            memos.c.is_archived == True
        ).order_by(memos.c.updated_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error(f"아카이브 메모 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="아카이브 메모 조회 중 오류가 발생했습니다.")


@app.get("/memos/list-favorites/", response_model=List[MemoInDB], summary="즐겨찾기 메모 조회")
async def list_favorite_memos(
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(100, ge=1, le=1000, description="반환할 최대 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = memos.select().where(
            memos.c.is_favorite == True
        ).order_by(memos.c.updated_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error(f"즐겨찾기 메모 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="즐겨찾기 메모 조회 중 오류가 발생했습니다.")


@app.get("/memos/list-by-author/", response_model=List[MemoInDB], summary="작성자별 메모 조회")
async def list_memos_by_author(
    author: str = Query(..., min_length=1, description="작성자"),
    skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
    limit: int = Query(100, ge=1, le=1000, description="반환할 최대 항목 수"),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = memos.select().where(
            memos.c.author == author
        ).order_by(memos.c.updated_at.desc()).offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.mappings().all()
    except Exception as e:
        logger.error(f"작성자별 메모 조회 중 오류 발생: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="작성자별 메모 조회 중 오류가 발생했습니다.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
