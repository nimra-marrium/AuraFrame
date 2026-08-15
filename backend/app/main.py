import logging
import sys
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Configure structured logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("auraframe")


# Create FastAPI application FIRST
app = FastAPI(
    title="AuraFrame API",
    description="AI Creative Workspace Backend API",
    version="0.1.0"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware for request logging & performance metrics
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(
        f"--> Incoming {request.method} request to {request.url.path}"
    )

    try:
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000

        logger.info(
            f"<-- Completed {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Duration: {process_time:.2f}ms"
        )

        return response

    except Exception as e:
        process_time = (time.time() - start_time) * 1000

        logger.error(
            f"X-- Failed {request.method} {request.url.path} "
            f"Error: {str(e)} "
            f"Duration: {process_time:.2f}ms",
            exc_info=True
        )

        raise


@app.get("/")
async def root():
    logger.info("Health check endpoint pinged.")

    return {
        "status": "online",
        "app": "AuraFrame API",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# --- Module routers ---
# Import routers AFTER the FastAPI app has been created.

from app.modules.auth.router import router as auth_router
from app.modules.brief_analyst.router import router as brief_analyst_router

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    brief_analyst_router,
    prefix="/agents/brief",
    tags=["agents"]
)


from app.modules.visual_analyst.router import router as visual_analyst_router
app.include_router(visual_analyst_router, prefix="/agents/visual", tags=["agents"])

from app.modules.collective_analyst.router import router as collective_analyst_router
app.include_router(collective_analyst_router, prefix="/agents/collective", tags=["agents"])