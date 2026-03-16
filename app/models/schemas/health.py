from app.models.schemas.rwschema import RWSchema


class HealthResponse(RWSchema):
    status: str
    version: str
    environment: str
