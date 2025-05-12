"""WebVH Log endpoints."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models.records import DidResourceRecord

from app.plugins import AskarStorage, WebVhProcessor

router = APIRouter(tags=["Resources"])
askar = AskarStorage()
webvh = WebVhProcessor()

@router.get("/resource")
async def return_cached_resource(scid: str, resourcePath: str):
    """Get known witnesses registry."""
    
    resource_id = f'{scid}{resourcePath}'
    resource = await askar.fetch("resourceRecord", resource_id)

    if not resource:
        raise HTTPException(status_code=404, detail="Unknown resource.")

    return JSONResponse(status_code=200, content=resource.get('resourceData'))

@router.post("/resource")
async def add_cached_resource(did: str, resourcePath: str):
    scid = did.split(':')[2]
    resource_id = f'{scid}{resourcePath}'
    resource = webvh.get_resource(did, resourcePath)
    if resource:
        resource_record = DidResourceRecord(
            scid=scid,
            resourcePath=resourcePath,
            resourceData=resource
        ).model_dump()
        await askar.store('resourceRecord', resource_id, resource_record)
    return JSONResponse(status_code=202, content={})