from fastapi import FastAPI, UploadFile, File, HTTPException, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from audio.audio_analysis import analyze_volume, NumpyEncoder
import json
import uuid
import os

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

def process_file(file_path: str, threshold_quiet_db: float, threshold_loud_db: float, job_id: str):
    try:
        results = analyze_volume(file_path, threshold_quiet_db, threshold_loud_db)
        job_results[job_id] = json.loads(json.dumps(results, cls=NumpyEncoder))
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
        background_tasks.add_task(process_file, file_path, threshold_quiet_db, threshold_loud_db, job_id)
        
        # Return the job ID immediately
        return JSONResponse(content={"job_id": job_id, "message": "Processing started"})
    
    except Exception as e:
        # If an error occurs, print stack trace and return error as JSON
        import traceback
        print(f"Error: {str(e)}")
        print("Stack trace:")
        traceback.print_exc()
        return JSONResponse(content={"error": str(e), "stack_trace": traceback.format_exc()}, status_code=500)

@app.get("/job_status/{job_id}")
async def get_job_status(job_id: str):
    if job_id in job_results:
        return JSONResponse(content={"status": "completed", "results": job_results[job_id]})
    else:
        return JSONResponse(content={"status": "processing"})
