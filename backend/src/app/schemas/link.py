from datetime import datetime

from pydantic import BaseModel, HttpUrl, Field


class LinkCreate(BaseModel):
    url: HttpUrl
    custom_slug : str | None = Field(default=None,max_length=12)
    expires_at: datetime | None = None


class LinkResponse(BaseModel):
    slug: str
    short_url: str
    original_url: str
    clicks_total: int
    expires_at: datetime | None
    created_at: datetime

    model_config = {
        "from_attributes" : True
    }