import os
import subprocess
import tempfile
from audio.audio_analysis import analyze_volume, NumpyEncoder
import json

def extract_audio(video_path):
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_audio_path = temp_audio.name
    temp_audio.close()

    try:
        subprocess.run(['ffmpeg', '-y', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', temp_audio_path], check=True)
        return temp_audio_path
    except subprocess.CalledProcessError:
        os.unlink(temp_audio_path)
        return None

def delete_audio(file_path):
    try:
        os.unlink(file_path)
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")

def process_audio(file_path: str, threshold_quiet_db: float, threshold_loud_db: float):
    
    results = analyze_volume(file_path, threshold_quiet_db, threshold_loud_db)
    return json.loads(json.dumps(results, cls=NumpyEncoder))
