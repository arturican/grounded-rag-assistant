"""FastAPI layer for the local grounded RAG pipeline."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.app.answering import GroundedAnswer, build_grounded_answer
from backend.app.cli import index_directory
from backend.app.embeddings import FakeEmbeddingProvider
from backend.app.index_store import load_index
from backend.app.retrieval import InMemoryRetrievalStore


class HealthResponse(BaseModel):
    """Liveness response for the API."""

    status: str


class IndexRequest(BaseModel):
    """Indexing request payload."""

    input_dir: str = Field(min_length=1)
    index_path: str = Field(min_length=1)


class IndexResponse(BaseModel):
    """Indexing response payload."""

    index_path: str
    indexed_chunk_count: int
    indexed_chunk_ids: list[str]


class AskRequest(BaseModel):
    """Question request payload."""

    index_path: str = Field(min_length=1)
    query: str = Field(min_length=1)
    top_k: int = Field(default=3, gt=0, le=10)


class AnswerSourceResponse(BaseModel):
    """Structured source returned with an answer."""

    source: str
    page: int | None
    chunk_id: str


class AskResponse(BaseModel):
    """Answer response payload."""

    answer: str
    used_context: bool
    sources: list[AnswerSourceResponse]


app = FastAPI(title="grounded-rag-assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return a simple health payload."""

    return HealthResponse(status="ok")


@app.post("/index", response_model=IndexResponse)
def index_documents(request: IndexRequest) -> IndexResponse:
    """Index supported documents from a local directory."""

    input_dir = Path(request.input_dir)

    if not input_dir.exists():
        raise HTTPException(
            status_code=404,
            detail=f"input_dir does not exist: {request.input_dir}",
        )

    if not input_dir.is_dir():
        raise HTTPException(
            status_code=400,
            detail=f"input_dir is not a directory: {request.input_dir}",
        )

    indexed_chunk_ids = index_directory(request.input_dir, request.index_path)
    return IndexResponse(
        index_path=str(Path(request.index_path)),
        indexed_chunk_count=len(indexed_chunk_ids),
        indexed_chunk_ids=indexed_chunk_ids,
    )


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest) -> AskResponse:
    """Answer a question strictly from the saved local index."""

    if not Path(request.index_path).exists():
        raise HTTPException(
            status_code=404,
            detail=f"index_path does not exist: {request.index_path}",
        )

    answer = _ask_grounded_question(request.index_path, request.query, top_k=request.top_k)
    return AskResponse(
        answer=answer.answer,
        used_context=answer.used_context,
        sources=[
            AnswerSourceResponse(source=source.source, page=source.page, chunk_id=source.chunk_id)
            for source in answer.sources
        ],
    )


def _ask_grounded_question(index_path: str | Path, query: str, *, top_k: int) -> GroundedAnswer:
    """Load a saved index and build a grounded answer for a query."""

    saved_index = load_index(index_path)
    store = InMemoryRetrievalStore(FakeEmbeddingProvider())
    store.load_indexed_chunks(saved_index.indexed_chunks)
    retrieved_chunks = store.search(query, top_k=top_k)
    return build_grounded_answer(retrieved_chunks, max_chunks=top_k, query=query)
