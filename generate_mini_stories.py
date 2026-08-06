import google.generativeai as genai
import json
import time
import os
from dotenv import load_dotenv

# Load API key from .env file (safe)
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please set it.")

INPUT_FILE = "top500_optimize.json"
OUTPUT_FILE = "enriched_stories.json"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def load_words(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_story(word):
    prompt = f"""You are an expert English teacher creating a mini-story for Bangla-speaking learners.
For the word "{word}", write:
1. A short, memorable story (2-3 sentences) that clearly shows the meaning and common usage of the word. 
2. A Bangla translation of the story.
3. A note about the word's tone (formal/informal/slang/offensive) if applicable.

Format your response EXACTLY as a JSON object with keys: "english_story", "bangla_story", "note".
Do not include any markdown or extra text."""
    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        if raw.startswith("```json"):
            raw = raw[7:-3]
        elif raw.startswith("```"):
            raw = raw[3:-3]
        return json.loads(raw)
    except Exception as e:
        print(f"Error for {word}: {e}")
        return None

def main():
    words = load_words(INPUT_FILE)
    enriched = {}
    for i, word in enumerate(words):
        print(f"Processing {i+1}/{len(words)}: {word}")
        data = generate_story(word)
        if data:
            enriched[word] = data
        time.sleep(1)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(enriched)} enriched stories to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()