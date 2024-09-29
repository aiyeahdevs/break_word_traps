from fastapi import FastAPI, UploadFile, File, HTTPException, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uuid
import os
from .job_processing import process_file

app = FastAPI()

# Transcription cache
transcription_cache = {}

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

# Mount a static directory to serve image files
app.mount("/images", StaticFiles(directory="api/images"), name="images")

@app.get("/")
async def root():
    return {"message": "Welcome to the Audio Analysis API"}

@app.post("/start-job/")
async def start_job(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...), 
    threshold_quiet_db: float = -30, 
    threshold_loud_db: float = -10,
    llmkey: str = Header(...)
):
    try:
        job_id = str(uuid.uuid4())
        file_path = f"temp_{job_id}_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        background_tasks.add_task(process_file, file_path, threshold_quiet_db, threshold_loud_db, job_id, llmkey, transcription_cache, job_results)
        
        return JSONResponse(content={"job_id": job_id, "message": "Processing started"})
    
    except Exception as e:
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
    
    result = job_results[job_id][task_name]
    if isinstance(result, str) and result.endswith('.png'):
        return FileResponse(f"images/{result}", media_type="image/png")
    else:
        return JSONResponse(content={task_name: result})
