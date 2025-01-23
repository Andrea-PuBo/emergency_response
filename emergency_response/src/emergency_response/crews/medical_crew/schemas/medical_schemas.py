from pydantic import BaseModel, Field
from typing import List

class MedicalTaskAssignment(BaseModel):
    """Output for analyzing emergency details."""
    ambulance_task: str = Field(..., description="Description of the ambulance task.")
    patient_priorities: List[str] = Field(..., description="List of patient priorities based on severity.")
    assigned_hospitals: List[str] = Field(..., description="List of hospitals assigned to receive patients.")

class Hospital(BaseModel):
    id: str = Field(..., description="Unique identifier for the hospital.")
    x_coordinate: float = Field(..., description="X coordinate of the hospital.")
    y_coordinate: float = Field(..., description="Y coordinate of the hospital.")

class HospitalsList(BaseModel):
    hospitals: List[Hospital] = Field(
        ..., description="A list of hospitals with their details."
    )

class TransportPlan(BaseModel):
    """Output for planning transport logistics."""
    ambulances: List[str] = Field(..., description="List of assigned ambulances.")
    routes: List[str] = Field(..., description="Planned routes for each ambulance.")

class PatientCarePlan(BaseModel):
    """Output for planning patient care."""
    prioritized_patients: List[str] = Field(..., description="List of prioritized patients based on severity.")
    care_details: str = Field(..., description="Details of patient care strategies.")

class CoordinatedMedicalPlan(BaseModel):
    """Output for coordinating transport and patient care plans."""
    transport_plan: str = Field(..., description="Integrated transport plan for ambulances.")
    patient_care_plan: str = Field(..., description="Integrated patient care plan.")

