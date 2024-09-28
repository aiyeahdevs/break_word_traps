from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from audio.audio_analysis import analyze_volume, NumpyEncoder
import json

app = FastAPI()

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

@app.post("/analyze_volume/")
async def analyze_audio_volume(
    file: UploadFile = File(...), 
    threshold_quiet_db: float = -30, 
    threshold_loud_db: float = -10,
    llmkey: str = Header(...)
):
    print(f"Received llmkey: {llmkey}")  # Print the received key
    try:
        # Save the uploaded file temporarily
        with open(file.filename, "wb") as buffer:
            buffer.write(await file.read())
        
        # Analyze the audio
        results = analyze_volume(file.filename, threshold_quiet_db, threshold_loud_db)
       
        # Clean up the temporary file
        import os
        os.remove(file.filename)
        
        # Return the results as JSON using NumpyEncoder
        return JSONResponse(content=json.loads(json.dumps(results, cls=NumpyEncoder)))
    
    except Exception as e:
        # If an error occurs, print stack trace and return error as JSON
        import traceback
        print(f"Error: {str(e)}")
        print("Stack trace:")
        traceback.print_exc()
        return JSONResponse(content={"error": str(e), "stack_trace": traceback.format_exc()}, status_code=500)
