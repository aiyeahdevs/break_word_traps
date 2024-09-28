from openai import OpenAI
import os

PROMPT_PATH = os.path.dirname(os.path.abspath(__file__))

def load_prompt(file_name: str) -> str:
    file_path = os.path.join(PROMPT_PATH, file_name)
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Using default prompt.")
        return "You are a helpful assistant."

def ask_llm(api_key: str, user_prompt_file: str, system_prompt_file: str) -> str:
    try:
        user_prompt = load_prompt(user_prompt_file)
        system_prompt = load_prompt(system_prompt_file)
    
        client = OpenAI(
            api_key=api_key
        )

        client = OpenAI(
        # This is the default and can be omitted
            api_key=api_key,
        )

        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return chat_completion.choices[0].message.content
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
    
    response = ask_llm(api_key, user_prompt, system_prompt)
    print(response)
