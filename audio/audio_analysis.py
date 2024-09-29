import ffmpeg
import librosa
import numpy as np
import sys
import os
import tempfile
import time
import warnings
import traceback
import json
import matplotlib.pyplot as plt

LOUDNESS_ANALYSIS_PATH = '/home/karol/Projects/break_word_traps/api/images/loudness_analysis.png'

# Ensure the directory exists
os.makedirs(os.path.dirname(LOUDNESS_ANALYSIS_PATH), exist_ok=True)

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.number):
            return float(obj)
        return super(NumpyEncoder, self).default(obj)

def delete_plot():
    if os.path.exists(LOUDNESS_ANALYSIS_PATH):
        os.remove(LOUDNESS_ANALYSIS_PATH)

def plot_loudness(sr, db, threshold_low, threshold_high):

    times = librosa.times_like(db, sr=sr, hop_length=int(1.0 * sr)//2)
    too_quiet = db < threshold_low
    too_loud = db > threshold_high

    results = []
    for i, (time, loudness) in enumerate(zip(times, db)):
        if too_quiet[i]:
            results.append((time, loudness, "Za cicho"))
        elif too_loud[i]:
            results.append((time, loudness, "Za głośno"))
        else:
            results.append((time, loudness, "OK"))

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
    plt.savefig(LOUDNESS_ANALYSIS_PATH)
    plt.close()

def analyze_volume(file_path, threshold_quiet_db, threshold_loud_db):
    print(f"Starting analysis of file: {file_path}")
    start_time = time.time()

    # Create a temporary WAV file
    temp_wav_path = tempfile.mktemp(suffix=".wav")

    try:
        print("Extracting audio from MP4 and converting to WAV...")
        # Extract audio from MP4 and convert to WAV using ffmpeg-python
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.output(stream, temp_wav_path, acodec='pcm_s16le', ac=1, ar='44100')
        try:
            out, err = ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"Conversion completed in {time.time() - start_time:.2f} seconds")
        except ffmpeg.Error as e:
            print(f"ffmpeg error output:\n{e.stderr.decode()}")
            raise

        print(f"Checking if WAV file was created: {os.path.exists(temp_wav_path)}")
        print(f"WAV file size: {os.path.getsize(temp_wav_path)} bytes")

        print("Loading WAV file...")
        # Load the WAV file
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            y, sr = librosa.load(temp_wav_path, sr=None)
        print(f"WAV file loaded in {time.time() - start_time:.2f} seconds")
        print(f"Audio length: {len(y) / sr:.2f} seconds")

        print("Calculating RMS energy...")
        # Calculate the RMS energy
        rms = librosa.feature.rms(y=y)
        print(f"RMS energy calculated in {time.time() - start_time:.2f} seconds")

        print("Calculating dB levels...")
        # Calculate dB levels
        db_levels = librosa.amplitude_to_db(rms[0])
        print(f"dB levels calculated in {time.time() - start_time:.2f} seconds")
        
        # Analyze volume
        too_loud = np.mean(db_levels > threshold_loud_db)
        too_quiet = np.mean(db_levels < threshold_quiet_db)

        print(f"Analysis completed in {time.time() - start_time:.2f} seconds")

        plot_loudness(sr, db_levels, threshold_quiet_db, threshold_loud_db)

        return {
            "too_loud_percentage": too_loud * 100,
            "too_quiet_percentage": too_quiet * 100,
            "average_db": np.mean(db_levels),
            "max_db": np.max(db_levels),
            "min_db": np.min(db_levels)
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(traceback.format_exc())
        raise
    finally:
        # Clean up temporary WAV file
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)
            print("Temporary WAV file removed")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python audio_analysis.py <path_to_mp4_file> <quiet_threshold_db> <loud_threshold_db>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    try:
        threshold_quiet_db = float(sys.argv[2])
        threshold_loud_db = float(sys.argv[3])
        results = analyze_volume(file_path, threshold_quiet_db, threshold_loud_db)

        # Convert results to a JSON string using the custom encoder
        json_results = json.dumps(results, indent=2, cls=NumpyEncoder)
        print(json_results)
    except ValueError as e:
        error_message = {"error": f"Invalid dB threshold values. {str(e)}"}
        print(json.dumps(error_message))
        sys.exit(1)
    except Exception as e:
        error_message = {"error": f"An error occurred during analysis: {str(e)}"}
        print(json.dumps(error_message, cls=NumpyEncoder))
        sys.exit(1)
