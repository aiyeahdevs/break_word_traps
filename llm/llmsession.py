from openai import OpenAI
import os
import re


def load_prompt(file_name: str) -> str:
    with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as file:
        return file.read().strip()

def ask_llm(api_key: str, user_prompt: str, system_prompt: str, is_thinking: bool = False) -> str:
    try:
        client = OpenAI(api_key=api_key)
       
        chat_completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        response = chat_completion.choices[0].message.content
        
        if is_thinking:
            answer_match = re.search(r'<answer>(.*?)</answer>', response, re.DOTALL)
            if answer_match:
                return answer_match.group(1).strip()
            else:
                return "No answer tag found in the response."
        else:
            return response
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python llmsession.py <api_key>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    user_prompt = load_prompt("user-prompt.txt")
    system_prompt = load_prompt("system-prompt.txt")
    
    response = ask_llm(api_key, user_prompt, system_prompt, is_thinking=True)
    print(response)

def transcribe_audio(api_key:str, file_path: str) -> str:
    try:
        print("Transcribing audio...")
        client = OpenAI(api_key=api_key)
        audio_file= open(file_path, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            language="pl"
        )
        print("transcriptn:" + transcription.text)
        return transcription.text
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}") 
        return ""
        
