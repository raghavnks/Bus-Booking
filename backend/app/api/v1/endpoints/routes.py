import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.route import RouteCreate, RouteRead
from app.services import route_service

router = APIRouter()


@router.get("", response_model=list[RouteRead])
def list_routes(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)) -> list[RouteRead]:
    return route_service.list_routes(db, limit=limit, offset=offset)


@router.post("", response_model=RouteRead, status_code=status.HTTP_201_CREATED)
def create_route(route_in: RouteCreate, db: Session = Depends(get_db)) -> RouteRead:
    return route_service.create_route(db, route_in)


@router.get("/{route_id}", response_model=RouteRead)
def get_route(route_id: uuid.UUID, db: Session = Depends(get_db)) -> RouteRead:
    route = route_service.get_route(db, route_id)
    if route is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    return route
