from pydantic import BaseModel, Field
from typing import List

class JSONParserSchema(BaseModel):
    json_file_type: str = Field(
        ..., description="The type of the json file loaded [hospitals or fire_trucks]"
    )

class FireTruck(BaseModel):
    id: str = Field(..., description="Unique identifier for the fire truck.")
    x_coordinate: float = Field(..., description="X coordinate of the fire truck.")
    y_coordinate: float = Field(..., description="Y coordinate of the fire truck.")

class FireTrucksList(BaseModel):
    fire_trucks: List[FireTruck] = Field(..., description="List of fire trucks.")

class Hospital(BaseModel):
    id: str = Field(..., description="Unique identifier for the hospital.")
    x_coordinate: float = Field(..., description="X coordinate of the hospital.")
    y_coordinate: float = Field(..., description="Y coordinate of the hospital.")

class HospitalsList(BaseModel):
    hospitals: List[Hospital] = Field(..., description="List of hospitals.")
