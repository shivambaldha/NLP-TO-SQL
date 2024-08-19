import os
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key = os.getenv("AssemblyAI_API_key")
transcriber = aai.Transcriber()

#set the URL/Local path
# Example use:
# local_path = './path/to/file.mp3'
# FILE_URL = "https://github.com/AssemblyAI-Community/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3

file_or_url = ""

transcript = transcriber.transcribe(file_or_url)

# print(transcript.text)
text_from_audio = transcript.text
print(text_from_audio)