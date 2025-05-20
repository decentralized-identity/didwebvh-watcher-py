"""WebVH Resource endpoints."""

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from app.models.records import DidResourceRecord

from app.plugins import AskarStorage, WebVhProcessor

router = APIRouter(tags=["Resources"])
askar = AskarStorage()
webvh = WebVhProcessor()


@router.get("/resource")
async def return_cached_resource(scid: str, resourcePath: str):
    """Get cached resource."""

    resource_id = f"{scid}{resourcePath}"
    resource = await askar.fetch("resourceRecord", resource_id)

    if not resource:
        raise HTTPException(status_code=404, detail="Unknown resource.")

    return Response(
        resource.get("resource_data"), media_type=resource.get("media_type")
    )


@router.post("/resource")
async def add_cached_resource(did: str, resourcePath: str):
    """Add/Update cached resource."""
    scid = did.split(":")[2]
    resource_id = f"{scid}{resourcePath}"
    resource_data, media_type = webvh.get_resource(did, resourcePath)
    if resource_data:
        resource_record = DidResourceRecord(
            scid=scid,
            media_type=media_type,
            resource_path=resourcePath,
            resource_data=resource_data,
        ).model_dump()

        if not await askar.fetch("resourceRecord", resource_id):
            await askar.store(
                "resourceRecord", resource_id, resource_record, {"scid": scid}
            )

        else:
            await askar.update(
                "resourceRecord", resource_id, resource_record, {"scid": scid}
            )

    return JSONResponse(status_code=202, content={})
