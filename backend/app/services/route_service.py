import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.route import Route
from app.schemas.route import RouteCreate


def list_routes(db: Session, limit: int = 50, offset: int = 0) -> list[Route]:
    stmt = select(Route).order_by(Route.origin).limit(limit).offset(offset)
    return list(db.execute(stmt).scalars().all())


def get_route(db: Session, route_id: uuid.UUID) -> Route | None:
    return db.get(Route, route_id)


def create_route(db: Session, route_in: RouteCreate) -> Route:
    route = Route(**route_in.model_dump())
    db.add(route)
    db.commit()
    db.refresh(route)
    return route
