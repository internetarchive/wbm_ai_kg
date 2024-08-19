import openai

openai.api_key =""
def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
    )

    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    prompt = "What is the capital of France?"
    response = ask_openai(prompt)
    print("OpenAI Response:", response)
