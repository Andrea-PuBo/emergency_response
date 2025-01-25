from pydantic import BaseModel, Field
from typing import List


class Hospital(BaseModel):
    id: str = Field(..., description="Unique identifier for the hospital.")
    x_coordinate: float = Field(..., description="X coordinate of the hospital.")
    y_coordinate: float = Field(..., description="Y coordinate of the hospital.")

class HospitalsList(BaseModel):
    hospitals: List[Hospital] = Field(
        ..., description="A list of hospitals with their details."
    )
class SelectedHospital(BaseModel):
    id: str = Field(..., description="Unique identifier for the hospital.")
    distance: float = Field(..., description="Distance of the hospital.")



