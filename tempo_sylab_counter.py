import whisper
from pydub import AudioSegment
import nltk
from nltk.corpus import cmudict

# Pobierz słownik CMU do liczenia sylab
nltk.download('cmudict')
d = cmudict.dict()

def count_syllables(word):
    try:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]])
    except KeyError:
        # Jeśli słowo nie jest w słowniku, szacujemy liczbę sylab na podstawie samogłosek
        return len(''.join(c for c in word if c in 'aeiouAEIOU'))

def analyze_speech_rate(video_path, segment_duration=30):
    # Ekstrakcja audio
    audio = AudioSegment.from_file(video_path, format="mp4")
    audio.export("temp_audio.wav", format="wav")

    # Transkrypcja
    model = whisper.load_model("base")
    result = model.transcribe("temp_audio.wav")

    total_syllables = 0
    total_duration = 0
    segments = []

    for segment in result["segments"]:
        text = segment["text"]
        duration = segment["end"] - segment["start"]
        words = text.split()
        syllables = sum(count_syllables(word) for word in words)

        total_syllables += syllables
        total_duration += duration

        speech_rate = syllables / duration if duration > 0 else 0
        segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": text,
            "speech_rate": speech_rate
        })

    overall_speech_rate = total_syllables / total_duration if total_duration > 0 else 0

    return overall_speech_rate, segments

# Przykładowe użycie
video_path = "sciezka/do/twojego/wideo.mp4"
overall_rate, segments = analyze_speech_rate(video_path)

print(f"Ogólne tempo mówienia: {overall_rate:.2f} sylab na sekundę")
print("\nAnaliza segmentów:")
for segment in segments:
    print(f"Czas: {segment['start']:.2f}s - {segment['end']:.2f}s")
    print(f"Tekst: {segment['text']}")
    print(f"Tempo mówienia: {segment['speech_rate']:.2f} sylab/s\n")
