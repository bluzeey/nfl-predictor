from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from pydantic import BaseModel,Field
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

class GamePrediction(BaseModel):
        team1: str
        team2: str
        probability_team1: float = Field(..., description="Win probability for team1")
        probability_team2: float = Field(..., description="Win probability for team2")
        key_factors: list[str] = Field(..., description="Key factors influencing the prediction")
        predicted_winner: str = Field(..., description="The team predicted to win")
        confidence_level: float = Field(..., description="Confidence in the prediction")

@CrewBase
class NflPredictor():
    """NflPredictor crew"""
    

    @before_kickoff
    def before_kickoff_function(self, inputs):
        team1 = input("Enter first NFL team: ")
        team2 = input("Enter second NFL team: ")
        inputs['team1'] = team1
        inputs['team2'] = team2
        print(f"\nAnalyzing matchup: {team1} vs {team2}")
        return inputs

    @after_kickoff
    def after_kickoff_function(self, result):
        try:
            print(result)
        except Exception as e:
            print(f"Unable to process prediction results: {e}")
        return result
    

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def stats_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['stats_analyst'],
            verbose=True
        )

    @agent
    def team_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['team_researcher'],
            verbose=True
        )

    @agent
    def matchup_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['matchup_analyst'],
            verbose=True
        )

    @agent
    def environmental_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['environmental_analyst'],
            verbose=True
        )

    @agent
    def prediction_synthesizer(self) -> Agent:
        return Agent(
            config=self.agents_config['prediction_synthesizer'],
            verbose=True
        )
    
    @task
    def statistical_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['statistical_analysis_task'],
            tools=[search_tool]
        )

    @task
    def team_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['team_research_task'],
            tools=[search_tool]
        )

    @task
    def matchup_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['matchup_analysis_task'],
            tools=[search_tool]
        )

    @task
    def environmental_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['environmental_analysis_task'],
            tools=[search_tool]
        )

    @task
    def prediction_synthesis_task(self) -> Task:
        return Task(
            config=self.tasks_config['prediction_synthesis_task'],
            output_json=GamePrediction
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )