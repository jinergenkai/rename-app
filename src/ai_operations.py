"""Handle AI operations using OpenAI's ChatGPT API."""

import os
import json
from typing import Optional, Tuple

import openai
from . import constants as c

def load_api_key() -> Optional[str]:
    """Load API key from file."""
    try:
        if os.path.exists(c.API_KEY_FILE):
            with open(c.API_KEY_FILE, 'r') as f:
                return f.read().strip()
    except Exception:
        pass
    return None

def save_api_key(api_key: str) -> None:
    """Save API key to file."""
    try:
        # Save with restricted permissions
        with open(c.API_KEY_FILE, 'w') as f:
            f.write(api_key)
        os.chmod(c.API_KEY_FILE, 0o600)
    except Exception as e:
        raise Exception(f"Không thể lưu API key: {str(e)}")

def generate_filename_and_summary(content: str) -> Tuple[str, str]:
    """Generate filename and summary using ChatGPT."""
    api_key = load_api_key()
    if not api_key:
        raise Exception(c.API_KEY_REQUIRED)
        
    # Limit content length
    if len(content) > c.MAX_CONTENT_CHARS:
        content = content[:c.MAX_CONTENT_CHARS] + "..."

    try:
        openai.api_key = api_key
        
        # Generate filename
        filename_response = openai.ChatCompletion.create(
            model=c.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a file naming assistant. Generate concise in under 10 word, descriptive filenames based on content."
                },
                {
                    "role": "user",
                    "content": c.AI_PROMPT.format(content=content)
                }
            ],
            temperature=0.7,
            max_tokens=50
        )
        
        # # Generate summary
        # summary_response = openai.ChatCompletion.create(
        #     model=c.OPENAI_MODEL,
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": "You are a content summarizer. Create brief, accurate summaries."
        #         },
        #         {
        #             "role": "user",
        #             "content": c.AI_SUMMARY_PROMPT.format(content=content)
        #         }
        #     ],
        #     temperature=0.7,
        #     max_tokens=50
        # )
        
        # Get the suggested filename and summary from responses
        filename = filename_response.choices[0].message.content.strip()
        summary = filename_response.choices[0].message.content.strip()
        
        # Clean up the responses
        filename = filename.replace('\n', ' ').strip()
        summary = summary.replace('\n', ' ').strip()
        
        if len(filename) > c.MAX_FILENAME_LENGTH:
            filename = filename[:c.MAX_FILENAME_LENGTH].strip()
            
        return filename, summary
        
    except Exception as e:
        raise Exception(f"Lỗi AI: {str(e)}")

def generate_filename(content: str) -> str:
    """Generate filename using ChatGPT (legacy support)."""
    filename, _ = generate_filename_and_summary(content)
    return filename