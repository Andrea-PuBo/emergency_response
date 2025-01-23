from pydantic import BaseModel, Field
from typing import List

class TaskAssignment(BaseModel):
    """Output for analyzing emergency details."""
    firefighting_task: str = Field(..., description="Description of the firefighting task.")
    rescue_task: str = Field(..., description="Description of the rescue task.")
    assigned_units: List[str] = Field(..., description="List of assigned units (e.g., trucks, personnel).")

class FireTruck(BaseModel):
    id: str = Field(..., description="Unique identifier for the fire truck.")
    x_coordinate: float = Field(..., description="X coordinate of the fire truck.")
    y_coordinate: float = Field(..., description="Y coordinate of the fire truck.")
class FireTrucksList(BaseModel):
    fire_trucks: List[FireTruck] = Field(
        ..., description="A list of fire trucks with their details."
    )

class FireSuppressionPlan(BaseModel):
    """Output for developing a fire suppression plan."""
    tools: List[str] = Field(..., description="List of tools required for firefighting.")
    strategy: str = Field(..., description="Fire suppression strategy based on the fire type and severity.")

class RescuePlan(BaseModel):
    """Output for developing a rescue plan."""
    priorities: List[str] = Field(..., description="List of prioritized individuals for rescue.")
    evacuation_routes: List[str] = Field(..., description="List of planned evacuation routes.")

class CoordinatedPlan(BaseModel):
    """Output for coordinating fire suppression and rescue plans."""
    firefighting_strategy: str = Field(..., description="Integrated firefighting strategy.")
    rescue_strategy: str = Field(..., description="Integrated rescue strategy.")
    notifications: List[str] = Field(..., description="Notifications sent to the respective units.")
