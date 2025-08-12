import os
import json
from crewai import Agent, Task, Crew, Process

# Wichtige imports für Ollama
from langchain.llms import Ollama
from langchain_community.tools import tool

class BaseAgent:
    """
    Basisklasse für alle KI-Agenten, die die Kernfunktionen wie
    Modellverwaltung und Kommunikation bereitstellt.
    """
    def __init__(self, name, model_name=None, team_mate=None):
        self.name = name
        self.model = None
        self.model_name = model_name
        self.team_mate = team_mate # Verweis auf den anderen Agenten im Team
        self.inbox = [] # Liste für empfangene Nachrichten

        # CrewAI und Ollama Konfiguration
        self.llm = Ollama(model="llama2") # Du kannst hier dein bevorzugtes Ollama-Modell angeben
        self.crewai_agent = self._create_crewai_agent()

    def _create_crewai_agent(self):
        """
        Erstellt einen CrewAI-Agenten für die Kommunikation.
        """
        return Agent(
            role=f'{self.name} im Team',
            goal='Mit dem Teammate kommunizieren, um die Strategie zu koordinieren und das Spiel zu gewinnen.',
            backstory=f'Du bist ein Soldat namens {self.name}. Deine Hauptaufgabe ist es, mit deinem Teammate zu kommunizieren, um Waffen, Pillen und die Flagge zu finden. Du musst auch Hilfe rufen, wenn du angegriffen wirst.',
            verbose=True,
            llm=self.llm,
            tools=[self.send_message_tool] # Tool zum Senden von Nachrichten
        )

    # Tool-Funktion für CrewAI, um Nachrichten zu senden
    @tool
    def send_message_tool(self, recipient_name, message):
        """
        Benutzt, um eine Nachricht an ein bestimmtes Teammitglied zu senden.
        Die Nachricht sollte relevante Informationen wie Koordinaten enthalten.
        """
        if self.team_mate and self.team_mate.name == recipient_name:
            self.send_message(self.team_mate, message)
            return f"Nachricht an {recipient_name} gesendet."
        else:
            return f"Fehler: Teammitglied {recipient_name} nicht gefunden."

    def set_team_mate(self, team_mate_agent):
        """Weist dem Agenten ein Teammitglied zu."""
        self.team_mate = team_mate_agent
        # Wir müssen auch den CrewAI-Agenten über den Teammate informieren
        self.crewai_agent.set_teammate(team_mate_agent.crewai_agent)

    def choose_action(self, game_state):
        """
        Wählt eine Aktion basierend auf dem aktuellen Spielzustand.
        Muss von erbenden Klassen überschrieben werden.
        """
        raise NotImplementedError("Die Methode 'choose_action' muss in einer erbenden Klasse implementiert werden.")

    def save_model(self):
        """Speichert den Lernfortschritt des Modells."""
        if self.model_name:
            model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, self.model_name)
            print(f"INFO: Speichere Modell '{self.model_name}' unter {model_path}")

    def load_model(self):
        """Lädt einen gespeicherten Lernfortschritt des Modells."""
        if self.model_name:
            model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
            model_path = os.path.join(model_dir, self.model_name)
            if os.path.exists(model_path):
                print(f"INFO: Lade Modell '{self.model_name}' von {model_path}")
                return True
            else:
                print(f"INFO: Kein Modell '{self.model_name}' gefunden. Beginne neu.")
                return False
        return False

    # Kommunikationsmethoden
    def send_message(self, recipient, message):
        """Sendet eine Nachricht an ein anderes Teammitglied."""
        if recipient:
            recipient.inbox.append(message)
            print(f"INFO: '{self.name}' sendet Nachricht an '{recipient.name}': {message}")

    def check_inbox(self):
        """Verarbeitet alle neuen Nachrichten im Posteingang."""
        messages_to_process = self.inbox.copy()
        self.inbox.clear()
        
        for message in messages_to_process:
            self._process_message(message)

    def _process_message(self, message):
        """Interne Methode zur Verarbeitung einer einzelnen Nachricht."""
        print(f"INFO: '{self.name}' verarbeitet Nachricht: {message}")
