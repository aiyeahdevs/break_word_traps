import numpy as np
import librosa
import matplotlib.pyplot as plt
from pydub import AudioSegment

def analyze_loudness(audio_path, segment_duration=1.0, threshold_low=-30, threshold_high=-10):
    # Wczytaj audio
    y, sr = librosa.load(audio_path)
    
    # Oblicz RMS (Root Mean Square) energii
    frame_length = int(segment_duration * sr)
    hop_length = frame_length // 2
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    
    # Konwertuj RMS na decybele
    db = librosa.amplitude_to_db(rms, ref=np.max)
    
    # Znajdź segmenty za ciche i za głośne
    times = librosa.times_like(db, sr=sr, hop_length=hop_length)
    too_quiet = db < threshold_low
    too_loud = db > threshold_high
    
    # Przygotuj wyniki
    results = []
    for i, (time, loudness) in enumerate(zip(times, db)):
        if too_quiet[i]:
            results.append((time, loudness, "Za cicho"))
        elif too_loud[i]:
            results.append((time, loudness, "Za głośno"))
        else:
            results.append((time, loudness, "OK"))
    
    return results, times, db

def plot_loudness(times, db, results, threshold_low, threshold_high):
    plt.figure(figsize=(15, 5))
    plt.plot(times, db)
    plt.axhline(y=threshold_low, color='r', linestyle='--', label='Próg ciszy')
    plt.axhline(y=threshold_high, color='g', linestyle='--', label='Próg głośności')
    
    for time, loudness, status in results:
        if status == "Za cicho":
            plt.plot(time, loudness, 'ro')
        elif status == "Za głośno":
            plt.plot(time, loudness, 'go')
    
    plt.xlabel('Czas (s)')
    plt.ylabel('Głośność (dB)')
    plt.title('Analiza głośności mowy')
    plt.legend()
    plt.tight_layout()
    plt.savefig('loudness_analysis.png')
    plt.close()

# Przykładowe użycie
audio_path = "sciezka/do/twojego/audio.wav"
threshold_low = -30  # dB
threshold_high = -10  # dB

results, times, db = analyze_loudness(audio_path, threshold_low=threshold_low, threshold_high=threshold_high)

print("Analiza głośności:")
for time, loudness, status in results:
    if status != "OK":
        print(f"Czas: {time:.2f}s, Głośność: {loudness:.2f}dB, Status: {status}")

plot_loudness(times, db, results, threshold_low, threshold_high)
print("Wykres analizy głośności został zapisany jako 'loudness_analysis.png'")