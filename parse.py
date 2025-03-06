import os
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

# Define the template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_deepseek(dom_chunks, parse_description):
    parsed_results = []
    
    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = template.format(dom_content=chunk, parse_description=parse_description)

        # Make a request to DeepSeek's API
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",  # Replace with the actual DeepSeek API endpoint
            headers={
                "Authorization": f"Bearer {deepseek_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",  # Replace with the correct model name
                "messages": [{"role": "system", "content": prompt}]
            }
        )

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            parsed_results.append(response_data["choices"][0]["message"]["content"])
        else:
            print(f"Failed to parse batch {i}: {response.status_code} - {response.text}")
            parsed_results.append("")

        print(f"Parsed batch: {i} of {len(dom_chunks)}")

    return "\n".join(parsed_results)