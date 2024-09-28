import ffmpeg
import librosa
import numpy as np
import sys
import os
import tempfile
import time

# Threshold values for volume analysis
THRESHOLD_LOUD = 0.1
THRESHOLD_QUIET = 0.01

def analyze_volume(file_path, threshold_loud=THRESHOLD_LOUD, threshold_quiet=THRESHOLD_QUIET):
    print(f"Starting analysis of file: {file_path}")
    start_time = time.time()

    # Create a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav_path = temp_wav.name

    try:
        print("Converting MP3 to WAV...")
        # Convert MP3 to WAV using ffmpeg-python
        stream = ffmpeg.input(file_path)
        stream = ffmpeg.output(stream, "./temp.wav")
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
        y, sr = librosa.load(temp_wav_path)
        print(f"WAV file loaded in {time.time() - start_time:.2f} seconds")
        print(f"Audio length: {len(y) / sr:.2f} seconds")

        print("Calculating RMS energy...")
        # Calculate the RMS energy
        rms = librosa.feature.rms(y=y)
        print(f"RMS energy calculated in {time.time() - start_time:.2f} seconds")

        # Normalize RMS
        rms_normalized = rms[0] / np.max(rms)

        print("Calculating dB levels...")
        # Calculate dB levels
        db_levels = librosa.amplitude_to_db(rms[0])
        print(f"dB levels calculated in {time.time() - start_time:.2f} seconds")
        
        # Analyze volume
        too_loud = np.mean(rms_normalized > threshold_loud)
        too_quiet = np.mean(rms_normalized < threshold_quiet)

        print(f"Analysis completed in {time.time() - start_time:.2f} seconds")
        return {
            "too_loud_percentage": too_loud * 100,
            "too_quiet_percentage": too_quiet * 100,
            "average_volume": np.mean(rms_normalized),
            "max_db": np.max(db_levels),
            "min_db": np.min(db_levels),
            "average_db": np.mean(db_levels)
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
    finally:
        # Clean up temporary WAV file
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)
            print("Temporary WAV file removed")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audio_analysis.py <path_to_audio_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    try:
        results = analyze_volume(file_path)

        print(f"\nAnalysis results for: {file_path}")
        print(f"Percentage of audio that's too loud: {results['too_loud_percentage']:.2f}%")
        print(f"Percentage of audio that's too quiet: {results['too_quiet_percentage']:.2f}%")
        print(f"Average volume: {results['average_volume']:.4f}")
        print(f"Maximum dB level: {results['max_db']:.2f} dB")
        print(f"Minimum dB level: {results['min_db']:.2f} dB")
        print(f"Average dB level: {results['average_db']:.2f} dB")
    except Exception as e:
        print(f"An error occurred during analysis: {str(e)}")
        sys.exit(1)
