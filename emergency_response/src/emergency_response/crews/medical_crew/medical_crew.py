from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools.file_read_tool.file_read_tool import FileReadTool
from ...tools.route_distance_tool import RouteDistanceTool

from .schemas.medical_schemas import  HospitalsList, SelectedHospital
import os

@CrewBase
class MedicalCrew:
    """Medical Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Load environmental variables from .env file
    hospitals_path = os.getenv("HOSPITALS_PATH")

    # Firefighting Coordinator Agent
    @agent
    def analyser_agent(self) -> Agent:
        """Firefighting analyser Agent."""
        return Agent(
            config=self.agents_config['analyser_agent'],
            llm='ollama/llama3.1',
            tools=[FileReadTool(file_path=self.hospitals_path)],
            max_iter=2,
            verbose=True
        )

    # Rescue Agent
    @agent
    def rescue_agent(self) -> Agent:
        """Rescue Agent."""
        return Agent(
            config=self.agents_config['rescue_agent'],
            llm='ollama/llama3.1',
            tools=[RouteDistanceTool()],
            max_iter=2,
            verbose=True
        )

    # Task Logic
    @task
    def analyse_hospitals(self) -> Task:
        """Analyzes firetrucks available"""
        return Task(
            config=self.tasks_config["analyse_hospitals"],
            output_pydantic=HospitalsList
        )

    @task
    def assign_hospitals(self) -> Task:
        return Task(
            config=self.tasks_config["assign_hospitals"],
            output_pydantic=SelectedHospital
        )

    # Crew Definition
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
