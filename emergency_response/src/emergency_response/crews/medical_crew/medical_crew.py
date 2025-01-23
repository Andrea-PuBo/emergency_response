from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from emergency_response.src.emergency_response.tools.route_distance_tool import RouteDistanceTool
from emergency_response.src.emergency_response.tools.json_parser_tool import JSONParserTool

from emergency_response.src.emergency_response.crews.medical_crew.schemas.medical_schemas import MedicalTaskAssignment, TransportPlan, PatientCarePlan, CoordinatedMedicalPlan, HospitalsList


@CrewBase
class MedicalCrew:
    """Medical Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Medical Coordinator Agent
    @agent
    def medical_coordinator_agent(self) -> Agent:
        """Medical Coordinator Agent."""
        return Agent(
            config=self.agents_config['medical_coordinator_agent'],
            llm='ollama/llama3.1',
			tools=[JSONParserTool(json_file_type="hospitals")],
            max_iter=3,
            verbose=True

        )

    # Ambulance Agent
    @agent
    def ambulance_agent(self) -> Agent:
        """Ambulance Agent."""
        return Agent(
            config=self.agents_config['ambulance_agent'],
            llm='ollama/llama3.1',
            tools=[RouteDistanceTool()],
            verbose=True
        )

    # Medical Agent
    @agent
    def medical_agent(self) -> Agent:
        """Medical Agent."""
        return Agent(
            config=self.agents_config['medical_agent'],
            llm='ollama/llama3.1',
            verbose=True
        )

    # Task Logic
    @task
    def analyse_emergency_details(self) -> Task:
        """Analyzes emergency details and assigns tasks to Medical crew members."""
        return Task(
            config=self.tasks_config["analyse_emergency_details"],
            output_pydantic=MedicalTaskAssignment
        )

    @task
    def load_hospitals(self) -> Task:
        """Analyzes emergency details and assigns tasks to Medical crew members."""
        return Task(
            config=self.tasks_config["load_hospitals"],
            output_pydantic=MedicalTaskAssignment
        )

    @task
    def plan_transport_logistics(self) -> Task:
        """Plans transport logistics for injured individuals."""
        return Task(
            config=self.tasks_config["develop_rescue_plan"],
            output_pydantic=TransportPlan
        )

    @task
    def plan_patient_care(self) -> Task:
        """Plans patient care strategies, including stabilization and hospital notifications."""
        return Task(
            config=self.tasks_config["plan_patient_care"],
            output_pydantic=PatientCarePlan
        )

    @task
    def coordinate_transport_and_patient_care(self) -> Task:
        """Coordinates transport and patient care plans into a unified medical response strategy."""
        return Task(
            config=self.tasks_config["coordinate_transport_and_patient_care"],
            output_pydantic=CoordinatedMedicalPlan
        )

    # Crew Definition
    @crew
    def crew(self) -> Crew:
        """Creates the Medical Crew with hierarchical process."""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.hierarchical,  # Hierarchical process for Coordinator-led task execution
            verbose=True,
        )
