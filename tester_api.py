# import requests

# # Replace with your OpenAI API key
# 
# model_name = "gpt-4"
# # Example of a simple API call to OpenAI
# response = requests.post(
#     "https://api.openai.com/v1/completions",
#     headers={
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     },
#     json={
#         "model": model_name,
#         "prompt": "Hello, world!",
#         "max_tokens": 5
#     }
# )

# # Print the relevant rate limit headers
# print("Rate Limit:", response.headers.get("X-RateLimit-Limit"))
# print("Rate Limit Remaining:", response.headers.get("X-RateLimit-Remaining"))
# print("Rate Limit Reset:", response.headers.get("X-RateLimit-Reset"))


import requests

# Replace with your OpenAI API key
api_key = ""
from datetime import datetime

# Define the date for which you want to retrieve usage data (format: YYYY-MM-DD)
# date = datetime.now().strftime('%Y-%m-%d')
date = "2024-08-07"  # Change to a date you know you've made API calls

# Make a request to the usage endpoint with the date parameter
response = requests.get(
    f"https://api.openai.com/v1/usage?date={date}",
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

# Check if the request was successful
if response.status_code == 200:
    usage_data = response.json()
    print("Usage data:", usage_data)
else:
    print("Failed to retrieve usage data:", response.status_code, response.text)
