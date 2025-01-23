from pydantic import BaseModel, Field

class FireEventSchema(BaseModel):
    """
    Schema for the parsed fire event details from an MDX file.
    """
    fire_type: str = Field(..., description="Type of fire (e.g., Electrical, Gas, etc.).")
    x_location: float = Field(..., description="X coordinate of the fire event.")
    y_location: float = Field(..., description="Y coordinate of the fire event.")
    injured_people: int = Field(..., description="Number of injured people reported.")
    severity: str = Field(..., description="Severity of the fire (e.g., Low, Medium, High).")