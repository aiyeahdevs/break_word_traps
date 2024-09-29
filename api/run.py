import sys
import os
import uvicorn
from dotenv import load_dotenv

# Print the current working directory
print("Current working directory:", os.getcwd())

# Print the Python path
print("Python path:", sys.path)

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
print("Added to Python path:", project_root)

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    print("Attempting to run Uvicorn...")
    port = int(os.getenv('BACK_PORT', 8000))  # Default to 8000 if API_PORT is not set
    host = os.getenv('BACK_HOST', "0.0.0.0")
    uvicorn.run("api.main:app", host=host, port=port, reload=True)
