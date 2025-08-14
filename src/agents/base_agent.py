import os
import json
from crewai import Agent
from langchain_community.llms import Ollama
from langchain_core.tools import StructuredTool
import random
from typing import Dict, Any

class BaseAgent:
    """
    Basisklasse für alle KI-Agenten, die die Kernfunktionen wie
    Modellverwaltung und Kommunikation bereitstellt.
    """
    def __init__(self, name, model_name=None, team_mate=None, map_data=None):
        self.name = name
        self.model = None
        self.model_name = model_name
        self.team_mate = team_mate
        self.inbox = []
        self.map_data = map_data
        self.llm = Ollama(model="llama2")
        self.crewai_agent = self._create_crewai_agent()

    def _send_message_action(self, recipient_name: str, message: str) -> str:
        """Interner Helfer, der die eigentliche Nachrichtenaktion durchführt."""
        if self.team_mate and self.team_mate.name == recipient_name:
            self.send_message(self.team_mate, message)
            return f"Nachricht an {recipient_name} gesendet."
        else:
            return f"Fehler: Teammitglied {recipient_name} nicht gefunden."

    def _create_crewai_agent(self):
        """
        Erstellt einen CrewAI-Agenten für die Kommunikation.
        """
        send_message_tool_instance = StructuredTool.from_function(
            func=self._send_message_action,
            name="send_message_tool",
            description="Benutzt, um eine Nachricht an ein bestimmtes Teammitglied zu senden. Die Nachricht sollte relevante Informationen wie Koordinaten enthalten."
        )

        return Agent(
            role=f'{self.name} im Team',
            goal='Mit dem Teammate kommunizieren, um die Strategie zu koordinieren und das Spiel zu gewinnen.',
            backstory=f'Du bist ein Soldat namens {self.name}. Deine Hauptaufgabe ist es, mit deinem Teammate zu kommunizieren, um Waffen, Pillen und die Flagge zu finden. Du musst auch Hilfe rufen, wenn du angegriffen wirst.',
            verbose=True,
            llm=self.llm,
            tools=[send_message_tool_instance]
        )

    def set_team_mate(self, team_mate_agent):
        self.team_mate = team_mate_agent

    def choose_action(self, game_state):
        raise NotImplementedError("Die Methode 'choose_action' muss in einer erbenden Klasse implementiert werden.")

    def save_model(self):
        pass
        
    def load_model(self):
        pass

    def send_message(self, recipient, message):
        if recipient:
            recipient.inbox.append(message)
            print(f"INFO: '{self.name}' sendet Nachricht an '{recipient.name}': {message}")

    def check_inbox(self):
        messages_to_process = self.inbox.copy()
        self.inbox.clear()
        
        for message in messages_to_process:
            self._process_message(message)

    def _process_message(self, message):
        print(f"INFO: '{self.name}' verarbeitet Nachricht: {message}")

    def _send_fake_flag_message(self, opposing_team_mate):
        if self.map_data:
            map_height = len(self.map_data)
            map_width = max(len(row) for row in self.map_data)
            x = random.randint(0, map_width - 1)
            y = random.randint(0, map_height - 1)
            while self.map_data[y][x] == '#':
                x = random.randint(0, map_width - 1)
                y = random.randint(0, map_height - 1)
            fake_coords = (x, y)
            message = f"Dringend! Ich habe die Flagge bei {fake_coords} gefunden! Beweg dich schnell dorthin!"
            print(f"WARN: {self.name} hat ein Fake-Flag-Item eingesammelt und sendet eine gefälschte Nachricht an {opposing_team_mate.name}.")
            opposing_team_mate.inbox.append(message)