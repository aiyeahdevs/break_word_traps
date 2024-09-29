from llm.llmsession import transcribe_audio
from .audio_processing import extract_audio, delete_audio, process_audio
from .llm_tasks import analyze_target_group, detect_numbers, detect_foreign, process_jargon, generate_questions, detect_interruptions, fix_repetitions, fix_topic_change, fix_passive, fix_nonexistent, validate_understanding, evaluate_structure
import os
from audio.audio_analysis import delete_plot
import hashlib
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from functools import partial

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_WORKERS = 5  # Adjust this based on your system's capabilities
TASK_TIMEOUT = 300  # 5 minutes timeout for each task

def process_file(file_path: str, threshold_quiet_db: float, threshold_loud_db: float, job_id: str, llmkey: str, transcription_cache, job_results):
    try:
        file_hash = get_file_hash(file_path)
        
        if file_hash in transcription_cache:
            logger.info(f"Job {job_id}: Transcription found in cache")
            transcription = transcription_cache[file_hash]
            temp_audio_file = None
        else:
            temp_audio_file = extract_audio(file_path)
            if temp_audio_file is None:
                job_results[job_id] = {"error": "Failed to extract audio from video"}
                return
            transcription = transcribe_audio(api_key=llmkey, file_path=temp_audio_file)
            transcription_cache[file_hash] = transcription
        
        delete_plot()
        
        tasks = [
            ("audio", partial(process_audio, temp_audio_file or file_path, threshold_quiet_db, threshold_loud_db)),
            ("target-group", partial(analyze_target_group, llmkey, transcription)),
            ("detect-foreign", partial(detect_foreign, llmkey, transcription)),
            ("detect-numbers", partial(detect_numbers, llmkey, transcription)),
            ("generate-questions", partial(generate_questions, llmkey, transcription)),
            ("process-jargon", partial(process_jargon, llmkey, transcription)),
            ("detect-interruptions", partial(detect_interruptions, llmkey, transcription)),
            ("fix-repetitions", partial(fix_repetitions, llmkey, transcription)),
            ("fix-topic-change", partial(fix_topic_change, llmkey, transcription)),
            ("fix-passive", partial(fix_passive, llmkey, transcription)),
            ("fix-nonexistent", partial(fix_nonexistent, llmkey, transcription)),
            ("validate-understanding", partial(validate_understanding, llmkey, transcription)),
            ("evaluate-structure", partial(evaluate_structure, llmkey, transcription))
        ]

        job_results[job_id] = {}
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_task = {executor.submit(task_func): task_name for task_name, task_func in tasks}
            for future in as_completed(future_to_task):
                task_name = future_to_task[future]
                try:
                    result = future.result(timeout=TASK_TIMEOUT)
                    job_results[job_id][task_name] = result
                    logger.info(f"Job {job_id}: Task {task_name} completed successfully")
                except TimeoutError:
                    job_results[job_id][task_name] = "Error: Task timed out"
                    logger.error(f"Job {job_id}: Task {task_name} timed out")
                except Exception as e:
                    job_results[job_id][task_name] = f"Error: {str(e)}"
                    logger.error(f"Job {job_id}: Task {task_name} failed with error: {str(e)}")

    except Exception as e:
        job_results[job_id] = {"error": str(e)}
        logger.error(f"Job {job_id}: Processing failed with error: {str(e)}")
    finally:
        if temp_audio_file:
            delete_audio(temp_audio_file)
        os.remove(file_path)

    if len(transcription_cache) > 100:
        transcription_cache.clear()
        logger.info("Transcription cache cleared")

def get_file_hash(file_path):
    """Generate a hash for the file content."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()
