from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel
from .crews.emergency_crew.emergency_crew import EmergencyCrew
from .crews.firefighting_crew.firefighting_crew import FirefightingCrew
from .crews.medical_crew.medical_crew import MedicalCrew

import json
import os
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, router, or_




class FireEventState(BaseModel):
    """
    Manages the state of the fire event throughout the flow.
    """
    location_x: float = None
    location_y: float = None
    injured_people: int = None
    fire_type: str = None
    fire_severity: str = None
    assigned_medical_unit_id: int = None
    assigned_firefighter_unit_id: int = None
    status: str = "initialized"


class FireEventFlow(Flow[FireEventState]):
    """
    Manages the fire response mechanism, combining the functionality of
    Emergency, Firefighting, and Medical Services crews.
    """

    @start()
    def read_fire_event_report(self) -> None:
        """
        Reads and parses the fire event report to initialize the state.
        """
        emergency_crew = EmergencyCrew()
        result = emergency_crew.crew().kickoff().raw
        parsed_result = json.loads(result)

        # Update state from parsed result
        self.state.location_x = parsed_result["x_location"]
        self.state.location_y = parsed_result["y_location"]
        self.state.injured_people = parsed_result["injured_people"]
        self.state.fire_type = parsed_result["fire_type"]
        self.state.fire_severity = parsed_result["severity"]

    @router(read_fire_event_report)
    def check_for_injured_people(self) -> str:
        """
        Routes the flow based on whether there are injured people.
        """
        return "Has Injured People" if self.state.injured_people > 0 else "No Injured People"

    def _assign_medical_units(self) -> int:
        """
        Assigns medical units for handling injured people.
        """
        medical_crew = MedicalCrew()
        result = medical_crew.crew().kickoff(
            inputs={
                "location_x": self.state.location_x,
                "location_y": self.state.location_y,
                "injured_people": self.state.injured_people,
            }
        ).raw
        return json.loads(result)["unit_id"]

    def _dispatch_firefighter_units(self) -> int:
        """
        Dispatches firefighter units based on the fire details.
        """
        firefighting_crew = FirefightingCrew()
        result = firefighting_crew.crew().kickoff(
            inputs={
                "location_x": self.state.location_x,
                "location_y": self.state.location_y,
                "fire_type": self.state.fire_type,
                "fire_severity": self.state.fire_severity,
            }
        ).raw
        return json.loads(result)["unit_id"]

    @listen("Has Injured People")
    def handle_event_with_injured_people(self) -> None:
        """
        Handles fire events with injured people by assigning both firefighter and medical units.
        """
        self.state.assigned_firefighter_unit_id = self._dispatch_firefighter_units()
        self.state.assigned_medical_unit_id = self._assign_medical_units()
        self.state.status = "both_units_assigned"

    @listen("No Injured People")
    def handle_event_without_injured_people(self) -> None:
        """
        Handles fire events without injured people by only assigning firefighter units.
        """
        self.state.assigned_firefighter_unit_id = self._dispatch_firefighter_units()
        self.state.assigned_medical_unit_id = None
        self.state.status = "only_firefighter_units_assigned"

    @listen(or_(handle_event_with_injured_people, handle_event_without_injured_people))
    def print_response_scenario(self) -> None:
        """
        Outputs the final response scenario, summarizing assigned units.
        """
        print(f"Assigned Firefighter Unit ID: {self.state.assigned_firefighter_unit_id}")
        if self.state.status == "both_units_assigned":
            print(f"Assigned Medical Unit ID: {self.state.assigned_medical_unit_id}")
        else:
            print("Assigned Medical Unit ID: Not Needed")


def kickoff() -> None:
    """
    Starts the FireEventFlow.
    """
    fire_event_flow = FireEventFlow()
    fire_event_flow.kickoff()


if __name__ == "__main__":
    kickoff()
