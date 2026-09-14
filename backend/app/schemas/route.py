import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RouteBase(BaseModel):
    origin: str = Field(min_length=1, max_length=100)
    destination: str = Field(min_length=1, max_length=100)
    distance_km: float = Field(gt=0)


class RouteCreate(RouteBase):
    pass


class RouteRead(RouteBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
