from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

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
            # Parse the result if it's a string
            if isinstance(result, str):
                import json
                result = json.loads(result)
            
            team1 = result.get('team1', '')
            team2 = result.get('team2', '')
            prob1 = float(result.get('probability_team1', 0))
            prob2 = float(result.get('probability_team2', 0))
            reasoning = result.get('reasoning', '')
            
            print("\nPrediction Results:")
            print(f"{team1}: {prob1:.1f}%")
            print(f"{team2}: {prob2:.1f}%")
            print(f"\nPredicted Winner: {team1 if prob1 > prob2 else team2}")
            print(f"\nKey Factors:\n{reasoning}")
        except Exception as e:
            print(f"Unable to process prediction results: {str(e)}")
            print(f"Raw result: {result}")
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
            config=self.tasks_config['statistical_analysis_task']
        )

    @task
    def team_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['team_research_task']
        )

    @task
    def matchup_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['matchup_analysis_task']
        )

    @task
    def environmental_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['environmental_analysis_task']
        )

    @task
    def prediction_synthesis_task(self) -> Task:
        return Task(
            config=self.tasks_config['prediction_synthesis_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )