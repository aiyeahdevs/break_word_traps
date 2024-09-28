from fastapi import FastAPI, UploadFile, File, HTTPException, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from audio.audio_analysis import analyze_volume, NumpyEncoder
from llm.llmsession import ask_llm
import json
import uuid
import os
import random

PROMPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../llm")

app = FastAPI()

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

def load_prompt(file_name: str) -> str:
    file_path = os.path.join(PROMPT_PATH, file_name)
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Using default prompt.")
        return "You are a helpful assistant."

def analyze_target_group(llmkey: str):
    
    user_prompt_file = "target-group-user.txt"
    system_prompt_file = "target-group-system.txt"
    
    user_prompt = load_prompt(user_prompt_file)
    system_prompt = load_prompt(system_prompt_file)
    
    # Use ask_llm to get the target group
    target_group = ask_llm(llmkey, user_prompt, system_prompt)
    
    return target_group.strip()

def process_file(file_path: str, threshold_quiet_db: float, threshold_loud_db: float, job_id: str, llmkey: str):
    tasks = [
        ("audio", lambda: process_audio(file_path, threshold_quiet_db, threshold_loud_db)),
        ("target-group", lambda: analyze_target_group(llmkey)),
    ]

    try:
        job_results[job_id] = {}
        for task_name, task_func in tasks:
            job_results[job_id][task_name] = task_func()
    except Exception as e:
        job_results[job_id] = {"error": str(e)}
    finally:
        os.remove(file_path)

@app.post("/start-job/")
async def start_job(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...), 
    threshold_quiet_db: float = -30, 
    threshold_loud_db: float = -10,
    llmkey: str = Header(...)
):
    print(f"Received llmkey: {llmkey}")  # Print the received key
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
