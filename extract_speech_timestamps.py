from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
import sys
model = load_silero_vad()
wav = read_audio(sys.argv[1])
speech_timestamps = get_speech_timestamps(wav, model)
for i in speech_timestamps:
    i['start'] = i['start']/16000
    i['end'] = i['end']/16000
print(speech_timestamps)
