import sys
import os                                                                                                                         
import uvicorn                                                                                                                    
                                                                                                                                
# Print the current working directory                                                                                             
print("Current working directory:", os.getcwd())                                                                                  
                                                                                                                                
# Print the Python path                                                                                                           
print("Python path:", sys.path)                                                                                                   
                                                                                                                                
# Add the project root to the Python path                                                                                         
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))                                                        
sys.path.append(project_root)                                                                                                     
print("Added to Python path:", project_root)                                                                                      
                                                                                                                                
if __name__ == "__main__":                                                                                                        
    print("Attempting to run Uvicorn...")                                                                                         
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)  