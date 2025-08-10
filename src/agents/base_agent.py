from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

class BaseAgent:
    def __init__(self, name, role, goal, backstory):
        # Das Ollama-Modell, das wir verwenden (hier 'llama3')
        # Stelle sicher, dass Ollama läuft und das Modell 'llama3' installiert ist.
        self.llm = Ollama(model="llama3")

        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        self.name = name

    def create_task(self, description, expected_output):
        return Task(
            description=description,
            expected_output=expected_output,
            agent=self.agent
        )

    def run_task(self, task):
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=2
        )
        result = crew.kickoff()
        return result