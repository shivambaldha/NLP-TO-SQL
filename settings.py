import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

@dataclass
class ENV:
    def __init__(self) -> None:
        """
        Initialise ENV class to load environment variables
        """
        self.ngrok = {
            "ngrok_api": os.getenv("NL_TO_SQL_API")
        }
        self.groq = {
            "groq_api": os.getenv("API_KEY_GROQ")
        }

env = ENV()
