import os
from llm.llmsession import ask_llm

PROMPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../llm/prompts")

def load_prompt(file_name: str) -> str:
    file_path = os.path.join(PROMPT_PATH, file_name)
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Using default prompt.")
        return "You are a helpful assistant."

def process_llm_task(llmkey: str, transcription: str, task_name: str, use_json: bool = False):
    try:
        print("Processing LLM task:", task_name)
        system_prompt_file = f"{task_name}-system.txt"
        system_prompt = load_prompt(system_prompt_file)
        
        result = ask_llm(llmkey, transcription, system_prompt, use_json)
        print(f"Result for {task_name}: {result}")
        return result.strip()
    except Exception as e:
        print(f"Error in process_llm_task for {task_name}: {str(e)}")
        raise

# Task-specific functions
def analyze_target_group(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "target-group", True)

def detect_numbers(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "detect-numbers")

def process_jargon(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "process-jargon", True)

def detect_foreign(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "detect-foreign")

def generate_questions(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "generate-questions", True)

def detect_interruptions(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "detect-interruptions")

def fix_repetitions(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "fix-repetitions")

def fix_topic_change(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "fix-topic-change")

def fix_passive(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "fix-passive")

def fix_nonexistent(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "fix-nonexistent")

def validate_understanding(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "validate-understanding", True)

def evaluate_structure(llmkey: str, transcription: str):
    return process_llm_task(llmkey, transcription, "evaluate-structure", True)


