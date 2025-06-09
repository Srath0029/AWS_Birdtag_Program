# query.py
from fastapi import APIRouter, HTTPException
from app.models.query_models import (
    TagsRequest,
    SearchBySpeciesRequest,
    SearchBySpeciesResponse,
    GetOriginalFromThumbnailRequest,
    GetOriginalFromThumbnailResponse,
)
from app.services.query_service import search_by_species, get_original_from_thumbnail, search_files_by_species_and_mincount

router = APIRouter()

@router.post("/search-by-species-and-mincount")
async def search_by_species_and_mincount(request: TagsRequest):
    try:
        urls = search_files_by_species_and_mincount(request.tags)
        return {"links": urls}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search-by-species", response_model=SearchBySpeciesResponse)
def search_species(request: SearchBySpeciesRequest):
    try:
        links = search_by_species(request.tags)
        return SearchBySpeciesResponse(links=links)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get-original-from-thumbnail", response_model=GetOriginalFromThumbnailResponse)
def get_original(request: GetOriginalFromThumbnailRequest):
    try:
        file_url = get_original_from_thumbnail(request.thumbnail_url)
        if not file_url:
            raise HTTPException(status_code=404, detail="Thumbnail URL not found.")
        return GetOriginalFromThumbnailResponse(file_url=file_url)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))