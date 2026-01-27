import os
import google.generativeai as genai

# Load API key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Give me 3 Python interview questions")

print(response.text)