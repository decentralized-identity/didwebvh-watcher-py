from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import admin, dids, resources
from config import settings

app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()


@api_router.get("/status", tags=["Server"], include_in_schema=False)
async def server_status():
    """Server status endpoint."""
    return JSONResponse(status_code=200, content={"status": "ok"})


api_router.include_router(admin.router)
api_router.include_router(dids.router)
api_router.include_router(resources.router)

app.include_router(api_router)
