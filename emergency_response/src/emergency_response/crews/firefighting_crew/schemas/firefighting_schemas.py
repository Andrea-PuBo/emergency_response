from pydantic import BaseModel, Field
from typing import List



class FireTruck(BaseModel):
    id: str = Field(..., description="Unique identifier for the fire truck.")
    x_coordinate: float = Field(..., description="X coordinate of the fire truck.")
    y_coordinate: float = Field(..., description="Y coordinate of the fire truck.")


class FireTrucksList(BaseModel):
    fire_trucks: List[FireTruck] = Field(
        ..., description="A list of fire trucks with their details."
    )

class SelectedFireTruck(BaseModel):
    id: str = Field(..., description="Unique identifier for the fire truck.")
    distance: float = Field(..., description="Distance of the fire truck.")


