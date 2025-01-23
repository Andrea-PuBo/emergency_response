from pydantic import BaseModel, Field

class RouteDistanceSchema(BaseModel):
    """Input schema for the RouteDistanceTool."""
    x_origin: float = Field(..., description="X coordinate of the origin location.")
    y_origin: float = Field(..., description="Y coordinate of the origin location.")
    x_destination: float = Field(..., description="X coordinate of the destination location.")
    y_destination: float = Field(..., description="Y coordinate of the destination location.")
