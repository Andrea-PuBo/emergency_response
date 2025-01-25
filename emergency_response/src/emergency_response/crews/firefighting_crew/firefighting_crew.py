from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools.file_read_tool.file_read_tool import FileReadTool
from ...tools.route_distance_tool import RouteDistanceTool

from .schemas.firefighting_schemas import FireTruck, FireTrucksList, SelectedFireTruck
import os


@CrewBase
class FirefightingCrew:
    """Firefighting Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Load environmental variables from .env file

    firetrucks_path = os.getenv("FIRETRUCKS_PATH")
    # Firefighting analyser Agent

    @agent
    def analyser_agent(self) -> Agent:
        """Firefighting analyser Agent."""
        return Agent(
            config=self.agents_config['analyser_agent'],
            llm='ollama/llama3.1',
            tools=[FileReadTool(file_path=self.firetrucks_path)],
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
    def analyse_firetrucks(self) -> Task:
        return Task(
            config=self.tasks_config["analyse_firetrucks"],
            output_pydantic=FireTrucksList
        )

    @task
    def assign_firetrucks(self) -> Task:

        return Task(
            config=self.tasks_config["assign_firetrucks"],
            output_pydantic=SelectedFireTruck
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
