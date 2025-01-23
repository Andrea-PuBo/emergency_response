from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from emergency_response.src.emergency_response.tools.route_distance_tool import RouteDistanceTool
from emergency_response.src.emergency_response.tools.json_parser_tool import JSONParserTool

from emergency_response.src.emergency_response.crews.firefighting_crew.schemas.firefighting_schemas import TaskAssignment, FireSuppressionPlan, RescuePlan, CoordinatedPlan, FireTrucksList



@CrewBase
class FirefightingCrew:
    """Firefighting Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Firefighting Coordinator Agent
    @agent
    def firefighting_coordinator_agent(self) -> Agent:
        """Firefighting Coordinator Agent."""
        return Agent(
            config=self.agents_config['firefighting_coordinator_agent'],
            llm='ollama/llama3.1',
            tools=[JSONParserTool(json_file_type="fire_trucks")],
            max_iter=3,
            verbose=True
        )

    # Firefighting Agent
    @agent
    def firefighting_agent(self) -> Agent:
        """Firefighting Agent."""
        return Agent(
            config=self.agents_config['firefighting_agent'],
            llm='ollama/llama3.1',
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
            verbose=True
        )

    # Task Logic
    @task
    def analyse_emergency_details(self) -> Task:
        """Analyzes fire details and assigns tasks to firefighting and rescue agents."""
        return Task(
            config=self.tasks_config["analyse_emergency_details"],
            output_pydantic=TaskAssignment
        )

    @task
    def load_fire_trucks(self) -> Task:

        return Task(
            config=self.tasks_config["load_fire_trucks"],
            output_pydantic=FireTrucksList
        )


    @task
    def develop_fire_suppression_plan(self) -> Task:
        """Develops a fire suppression plan based on fire type, severity, and location."""
        return Task(
            config=self.tasks_config["develop_fire_suppression_plan"],
            output_pydantic=FireSuppressionPlan
        )

    @task
    def develop_rescue_plan(self) -> Task:
        """Develops a rescue plan including evacuation routes and priorities."""
        return Task(
            config=self.tasks_config["develop_rescue_plan"],
            output_pydantic=RescuePlan
        )

    @task
    def coordinate_fire_suppression_and_rescue(self) -> Task:
        """Coordinates fire suppression and rescue plans into a cohesive strategy."""
        return Task(
            config=self.tasks_config["coordinate_fire_suppression_and_rescue"],
            output_pydantic=CoordinatedPlan
        )

    # Crew Definition
    @crew
    def crew(self) -> Crew:
        """Creates the Firefighting Crew with hierarchical process."""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.hierarchical,  # Hierarchical process for Coordinator-led task execution
            verbose=True,
        )
