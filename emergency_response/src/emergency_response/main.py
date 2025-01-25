from crewai.flow.flow import Flow, listen, start, router, or_
from pydantic import BaseModel
from .crews.emergency_crew.emergency_crew import EmergencyCrew
from .crews.firefighting_crew.firefighting_crew import FirefightingCrew
from .crews.medical_crew.medical_crew import MedicalCrew

import json
import os

from dotenv import load_dotenv
load_dotenv()


EMERGENCY_REPORT_PATH: str = os.getenv("EMERGENCY_REPORT_PATH", "emergency_01.mdx")
FIRETRUCKS_PATH = os.getenv("FIRETRUCKS_PATH", "firetrucks.json")
HOSPITALS_PATH = os.getenv("HOSPITALS_PATH", "hospitals.json")

class EmergencyEventState(BaseModel):

    x_location: float = None
    y_location: float = None
    injured_people: int = None
    fire_type: str = None
    severity: str = None
    assigned_hospital_id: str = None
    assigned_firetruck_id: str = None
    firetruck_distance: float = None  # Add firetruck distance
    hospital_distance: float = None
    status: "str" = "notified"


class EmergencyEventFlow(Flow[EmergencyEventState]):


    @start()
    def receive_emergency_details(self) -> None:
        """
        Reads and parses the fire event report to initialize the state.
        """
        _r = (
            EmergencyCrew()
            .crew()
            .kickoff(inputs={"mdx_file": EMERGENCY_REPORT_PATH})
        )
        result = json.loads(_r.raw)
        self.state.x_location = result["x_location"]
        self.state.y_location = result["y_location"]
        self.state.injured_people = result["injured_people"]
        self.state.fire_type = result["fire_type"]
        self.state.severity = result["severity"]

    @router(receive_emergency_details)
    def check_for_injured_people(self) -> "str":
        if self.state.injured_people > 0:
            return "Medical Crew Required"
        else:
            return "No Medical Crew Required"


    def _assign_firetrucks(self) -> tuple[str, float]:
        """
            Assign a firetruck to the fire event and return its ID and distance.

            Returns:
                tuple[str, float]: A tuple containing the firetruck ID and distance.
            """
        _r = (
            FirefightingCrew()
            .crew()
            .kickoff(
                inputs={
                    "json_file": FIRETRUCKS_PATH,
                    "x_location": self.state.x_location,
                    "y_location": self.state.y_location,
                    "fire_type": self.state.fire_type,
                    "severity": self.state.severity,
                }
            )
        )
        result = json.loads(_r.raw)
        return result["id"], result["distance"]

    def _assign_hospitals(self) -> tuple[str, float]:
        _r = (
            MedicalCrew()
            .crew()
            .kickoff(
                inputs={
                    "json_file": HOSPITALS_PATH,
                    "x_location": self.state.x_location,
                    "y_location": self.state.y_location,
                    "injured_people": self.state.injured_people,
                }
            )
        )
        result = json.loads(_r.raw)
        return result["id"], result["distance"]

    @listen("Medical Crew Required")
    def emergency_with_medical_crew(self) -> "None":
        firetruck_id, firetruck_distance = self._assign_firetrucks()
        hospital_id, hospital_distance = self._assign_hospitals()

        # Store IDs and distances in the state
        self.state.assigned_firetruck_id = firetruck_id
        self.state.firetruck_distance = firetruck_distance
        self.state.assigned_hospital_id = hospital_id
        self.state.hospital_distance = hospital_distance
        self.state.status = "both_crews_assigned"

    @listen("No Medical Crew Required")
    def emergency_without_medical_crew(self) -> "None":
        firetruck_id, firetruck_distance = self._assign_firetrucks()

        # Store ID and distance for firetruck, hospital is None
        self.state.assigned_firetruck_id = firetruck_id
        self.state.firetruck_distance = firetruck_distance
        self.state.assigned_hospital_id = None
        self.state.hospital_distance = None
        self.state.status = "only_firefighting_crew_assigned"

    @listen(or_(emergency_with_medical_crew, emergency_without_medical_crew))
    def print_response(self) -> "None":
        print(
            f"Assigned Firetruck: {self.state.assigned_firetruck_id} (Distance: {self.state.firetruck_distance} km)"
        )
        if self.state.status == "both_crews_assigned":
            print(
                f"Assigned Hospital: {self.state.assigned_hospital_id} (Distance: {self.state.hospital_distance} km)"
            )
        else:
            print("Assigned Hospital: Not Needed")


def kickoff() -> None:

    emergency_event_flow = EmergencyEventFlow()
    emergency_event_flow.kickoff()


if __name__ == "__main__":
    kickoff()
