from openai import OpenAI
import os

def ask_llm(api_key: str, user_prompt: str, system_prompt: str) -> str:
    try:
       
    
        client = OpenAI(
            api_key=api_key
        )

        client = OpenAI(
        # This is the default and can be omitted
            api_key=api_key,
        )
        print("api_key" + api_key) 
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
