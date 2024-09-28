from pydub import AudioSegment
import librosa
import numpy as np

def analyze_volume(file_path, threshold_loud=0.1, threshold_quiet=0.01):
    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(file_path)
    audio.export("temp.wav", format="wav")

    # Load the WAV file
    y, sr = librosa.load("temp.wav")

    # Calculate the RMS energy
    rms = librosa.feature.rms(y=y)

    # Normalize RMS
    rms_normalized = rms[0] / np.max(rms)

    # Analyze volume
    too_loud = np.mean(rms_normalized > threshold_loud)
    too_quiet = np.mean(rms_normalized < threshold_quiet)

    return {
        "too_loud_percentage": too_loud * 100,
        "too_quiet_percentage": too_quiet * 100,
        "average_volume": np.mean(rms_normalized)
    }

if __name__ == "__main__":
    # Example usage
    file_path = "path/to/your/audio.mp3"
    results = analyze_volume(file_path)

    print(f"Percentage of audio that's too loud: {results['too_loud_percentage']:.2f}%")
    print(f"Percentage of audio that's too quiet: {results['too_quiet_percentage']:.2f}%")
    print(f"Average volume: {results['average_volume']:.4f}")
