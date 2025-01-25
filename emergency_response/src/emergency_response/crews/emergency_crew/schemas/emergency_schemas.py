from pydantic import BaseModel, Field
from typing import List, Optional
#from ...firefighting_crew.schemas.firefighting_schemas import FireSuppressionPlan, RescuePlan
#from ...medical_crew.schemas.medical_schemas import TransportPlan, PatientCarePlan

class EmergencyDetails(BaseModel):
    """Schema for the emergency mdx file details."""
    fire_type: str = Field(..., description="Type of fire (e.g., ordinary, electrical).")
    x_location: float = Field(..., description="X coordinate of the fire's location.")
    y_location: float = Field(..., description="Y coordinate of the fire's location.")
    injured_people: int = Field(..., description="Number of injured individuals.")
    severity: str = Field(..., description="Severity of the fire (e.g., low, medium, high).")


