from pydantic import BaseModel, Field
from typing import List, Optional
from emergency_response.src.emergency_response.crews.firefighting_crew.schemas.firefighting_schemas import FireSuppressionPlan, RescuePlan
from emergency_response.src.emergency_response.crews.medical_crew.schemas.medical_schemas import TransportPlan, PatientCarePlan

class EmergencyDetails(BaseModel):
    """Schema for the emergency mdx file details."""
    fire_type: str = Field(..., description="Type of fire (e.g., ordinary, electrical).")
    x_location: float = Field(..., description="X coordinate of the fire's location.")
    y_location: float = Field(..., description="Y coordinate of the fire's location.")
    injured_people: int = Field(..., description="Number of injured individuals.")
    severity: str = Field(..., description="Severity of the fire (e.g., low, medium, high).")

class IncidentAnalysis(BaseModel):
    """Schema for analyzing the incident and assigning tasks."""
    crews_assigned: List[str] = Field(..., description="List of assigned crews (e.g., firefighting, medical).")
    priority: int = Field(..., description="Priority level of the incident.")
    categorization_details: str = Field(..., description="Details about the incident categorization process.")

class CrewNotification(BaseModel):
    """Schema for notifying the crews about the emergency."""
    crew: str = Field(..., description="Name of the crew notified (e.g., firefighting, medical).")
    message: str = Field(..., description="Notification message sent to the crew.")
    status: str = Field(..., description="Status of the notification (e.g., sent, acknowledged).")

class FinalPlan(BaseModel):
    """Schema for the final emergency response plan."""
    firefighting_plan: Optional[FireSuppressionPlan] = Field(None, description="Details of the firefighting crew's plan.")
    rescue_plan: Optional[RescuePlan] = Field(None, description="Details of the rescue plan developed by the firefighting crew.")
    transport_plan: Optional[TransportPlan] = Field(None, description="Details of the medical crew's transport plan.")
    patient_care_plan: Optional[PatientCarePlan] = Field(None, description="Details of the medical crew's patient care plan.")
    overall_plan_summary: Optional[str] = Field(None, description="Summary of the overall emergency response plan.")