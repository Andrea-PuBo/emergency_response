from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from ...tools.mdx_parser_tool import MDXParserTool
from .schemas.emergency_schemas import EmergencyDetails



@CrewBase
class EmergencyCrew:
    """Emergency Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Emergency Agent
    @agent
    def coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config["coordinator"],
            tools=[MDXParserTool()],
            llm='ollama/llama3.1',
            max_iter=2,
            verbose=True
        )


    @task
    def provide_emergency_details(self) -> Task:
        return Task(
            config=self.tasks_config["provide_emergency_details"],
            output_pydantic=EmergencyDetails
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
