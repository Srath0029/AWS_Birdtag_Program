from pydantic import BaseModel
from typing import Dict, Optional, List

class TagsRequest(BaseModel):
    tags: Dict[str, int]  # e.g. {"crow": 3, "pigeon": 2}

class SearchBySpeciesRequest(BaseModel):
    tags: Dict[str, bool]

class SearchBySpeciesResponse(BaseModel):
    links: List[str]

class GetOriginalFromThumbnailRequest(BaseModel):
    thumbnail_url: str

class GetOriginalFromThumbnailResponse(BaseModel):
    file_url: Optional[str]

class TagEntry(BaseModel):
    tag: str
    count: int

class TagManagementRequest(BaseModel):
    url: Optional[List[str]] = None   # Accept list of URLs or singular URLs
    urls: Optional[List[str]] = None
    operation: int                    # 0 = decrement, 1 = increment
    tags: List[str]                  # Format "tag_name,count"

class TagManagementResponse(BaseModel):
    message: str
