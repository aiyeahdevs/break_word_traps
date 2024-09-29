from fastapi import FastAPI, UploadFile, File, HTTPException, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from audio.audio_analysis import analyze_volume, NumpyEncoder
from llm.llmsession import ask_llm, transcribe_audio
import json
import uuid
import os
import random
import subprocess
import tempfile
import hashlib

PROMPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../llm")

app = FastAPI()

# Transcription cache
transcription_cache = {}

def get_file_hash(file_path):
    """Generate a hash for the file content."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def extract_audio(video_path):
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_audio_path = temp_audio.name
    temp_audio.close()

    try:
        subprocess.run(['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', temp_audio_path], check=True)
        return temp_audio_path
    except subprocess.CalledProcessError:
        os.unlink(temp_audio_path)
        return None

def delete_audio(file_path):
    try:
        os.unlink(file_path)
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")

def extract_audio(video_path):
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_audio_path = temp_audio.name
    temp_audio.close()

    try:                                                                                                    
         subprocess.run(['ffmpeg', '-y', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100',    
 '-ac', '2', temp_audio_path], check=True)                                                                   
         return temp_audio_path                                                                              
    except subprocess.CalledProcessError:                                                                   
         os.unlink(temp_audio_path)                                                                          
         return None  

def delete_audio(file_path):
    try:
        os.unlink(file_path)
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")

# Store job results
job_results = {}

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Audio Analysis API"}

def process_audio(file_path: str, threshold_quiet_db: float, threshold_loud_db: float):
    results = analyze_volume(file_path, threshold_quiet_db, threshold_loud_db)
    return json.loads(json.dumps(results, cls=NumpyEncoder))

def analyze_target_group(llmkey: str, transcription: str): 
    # user_prompt_file = "target-group-user.txt"
    system_prompt_file = "target-group-system.txt"
    
    # user_prompt = load_prompt(user_prompt_file)
    user_prompt = transcription
    system_prompt = load_prompt(system_prompt_file)
    
    # Use ask_llm to get the target group
    target_group = ask_llm(llmkey, user_prompt, system_prompt, True)
    
    return target_group.strip()

def detect_numbers(llmkey: str, transcription: str):
    #user_prompt_file = "target-group-user.txt"
    system_prompt_file = "detect-numbers-system.txt"
    
    #user_prompt = load_prompt(user_prompt_file)
    user_prompt = transcription
    system_prompt = load_prompt(system_prompt_file)
    
    # Use ask_llm to get the target group
    target_group = ask_llm(llmkey, user_prompt, system_prompt, False)
    
    return target_group.strip()

def load_prompt(file_name: str) -> str:
    file_path = os.path.join(PROMPT_PATH, file_name)
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Using default prompt.")
        return "You are a helpful assistant."

def process_file(file_path: str, threshold_quiet_db: float, threshold_loud_db: float, job_id: str, llmkey: str):
    try:
        # Generate a hash for the video file
        file_hash = get_file_hash(file_path)
        
        # Check if transcription is in cache
        if file_hash in transcription_cache:
            print("Transcription found in cache")
            transcription = transcription_cache[file_hash]
            temp_audio_file = None
        else:
            temp_audio_file = extract_audio(file_path)
            if temp_audio_file is None:
                job_results[job_id] = {"error": "Failed to extract audio from video"}
                return
            transcription = transcribe_audio(api_key=llmkey, file_path=temp_audio_file)
            # Store in cache
            transcription_cache[file_hash] = transcription

        tasks = [
            ("audio", lambda: process_audio(temp_audio_file or file_path, threshold_quiet_db, threshold_loud_db)),
            ("target-group", lambda: analyze_target_group(llmkey, transcription)),
            ("detect-numbers", lambda: detect_numbers(llmkey, transcription))]

        job_results[job_id] = {}
        for task_name, task_func in tasks:
            job_results[job_id][task_name] = task_func()
    except Exception as e:
        job_results[job_id] = {"error": str(e)}
    finally:
        if temp_audio_file:
            delete_audio(temp_audio_file)
        os.remove(file_path)

    # Optionally, clear cache if it gets too large
    if len(transcription_cache) > 100:
        transcription_cache.clear()

@app.post("/start-job/")
async def start_job(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...), 
    threshold_quiet_db: float = -30, 
    threshold_loud_db: float = -10,
    llmkey: str = Header(...)
):
    try:
        # Generate a unique job ID
        job_id = str(uuid.uuid4())
        
        # Save the uploaded file temporarily
        file_path = f"temp_{job_id}_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Start the background task
        background_tasks.add_task(process_file, file_path, threshold_quiet_db, threshold_loud_db, job_id, llmkey)
        
        # Return the job ID immediately
        return JSONResponse(content={"job_id": job_id, "message": "Processing started"})
    
    except Exception as e:
        # If an error occurs, print stack trace and return error as JSON
        import traceback
        print(f"Error: {str(e)}")
        print("Stack trace:")
        traceback.print_exc()
        return JSONResponse(content={"error": str(e), "stack_trace": traceback.format_exc()}, status_code=500)

@app.get("/job-status/{job_id}")
async def get_job_status(job_id: str):
    if job_id in job_results:
        return JSONResponse(content={"status": "completed", "results": job_results[job_id]})
    else:
        return JSONResponse(content={"status": "processing"})

@app.get("/job-result/{job_id}/{task_name}")
async def get_job_result(job_id: str, task_name: str):
    if job_id not in job_results:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if task_name not in job_results[job_id]:
        raise HTTPException(status_code=404, detail=f"Task '{task_name}' not found in job results")
    
    return JSONResponse(content={task_name: job_results[job_id][task_name]})
