from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from emergency_response.src.emergency_response.tools.mdx_parser_tool import MDXParserTool
from emergency_response.src.emergency_response.crews.emergency_crew.schemas.emergency_schemas import EmergencyDetails, IncidentAnalysis, CrewNotification, FinalPlan
import json


@CrewBase
class EmergencyCrew:
    """Emergency Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Emergency Agent
    @agent
    def emergency_agent(self) -> Agent:
        """Emergency Agent."""
        return Agent(
            config=self.agents_config['emergency_agent'],
            tools=[MDXParserTool()],
            llm='ollama/llama3.1',
            verbose=True
        )

    # Task Logic
    @task
    def receive_emergency_details(self) -> Task:
        """Coordinates fire suppression and rescue plans into a cohesive strategy."""
        return Task(
            config=self.tasks_config["receive_emergency_details"],
            output_pydantic=EmergencyDetails
        )

    @task
    def analyse_incident(self) -> Task:
        """Coordinates fire suppression and rescue plans into a cohesive strategy."""
        return Task(
            config=self.tasks_config["analyse_incident"],
            output_pydantic=IncidentAnalysis
        )

    @task
    def notify_crews(self) -> Task:
        """Coordinates fire suppression and rescue plans into a cohesive strategy."""
        return Task(
            config=self.tasks_config["notify_crews"],
            output_pydantic=CrewNotification
        )

    @task
    def finalize_plan(self) -> Task:
        """Coordinates fire suppression and rescue plans into a cohesive strategy."""
        return Task(
            config=self.tasks_config["finalize_plan"],
            output_pydantic=FinalPlan
        )


    # Crew Definition
    @crew
    def crew(self) -> Crew:
        """Creates the Emergency Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
