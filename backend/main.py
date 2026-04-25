"""MühendisAl Platform Backend — FastAPI ana giriş."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .database import init_db, SessionLocal
from .rate_limit import limiter
from .routes import auth, progress, quiz, streak_feedback, xp
from . import models


app = FastAPI(
    title="MühendisAl Platform API",
    version="0.2.0",
    description="AI Engineer öğrenme platformu — FAZ D rate limit eklendi",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Rate limiter state + exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# CORS — wiki.oluk.org'dan widget JS'leri çağırabilsin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://wiki.oluk.org",
        "http://localhost:8000",  # mkdocs serve test
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    """POST /api/* isteklerini api_log tablosuna yaz."""
    response = await call_next(request)
    if request.method == "POST" and request.url.path.startswith("/api/"):
        try:
            db = SessionLocal()
            ip = request.client.host if request.client else None
            db.add(models.ApiLog(
                ip=ip,
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code,
            ))
            db.commit()
            db.close()
        except Exception:
            pass  # log kaybı kullanıcı isteğini etkilemesin
    return response


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "muhendisal-api", "version": "0.2.0"}


# Router'ları kaydet
app.include_router(auth.router)
app.include_router(progress.router)
app.include_router(quiz.router)
app.include_router(streak_feedback.router)
app.include_router(xp.router)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # Rate limit istisnaları kendi handler'ında yakalanıyor; bu sadece güvenlik ağı
    if isinstance(exc, RateLimitExceeded):
        raise exc
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": exc.__class__.__name__},
    )
