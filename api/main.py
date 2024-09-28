from fastapi import FastAPI, UploadFile, File


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Audio Analysis API"}

@app.post("/analyze_volume/")
async def analyze_audio_volume(file: UploadFile = File(...), threshold_quiet_db: float = -30, threshold_loud_db: float = -10):
    # Save the uploaded file temporarily
    # with open(file.filename, "wb") as buffer:
    #     buffer.write(await file.read())
    
    # # Analyze the audio
    # results = analyze_volume(file.filename, threshold_quiet_db, threshold_loud_db)
    
    # # Clean up the temporary file
    # import os
    # os.remove(file.filename)
    
    return results
