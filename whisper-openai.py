from openai import OpenAI
import sys
client = OpenAI()

audio_file = open(sys.argv[1], "rb")
transcript = client.audio.transcriptions.create(
	file = audio_file,
	model="whisper-1",
	response_format="verbose_json",
	timestamp_granularities=["word"],
	language="pl"
)

print(transcript.words)
#print(transcript)
