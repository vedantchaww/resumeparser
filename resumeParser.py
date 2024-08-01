import openai
import tkinter as tk
from tkinter import filedialog

# Initialize OpenAI API key
openai.api_key = "api-key-here"

# Function to parse resume text to JSON using ChatGPT
def parse_resume_to_json(resume_text):
    prompt = f"""
    Take the following resume text as input and parse the content into JSON format:
    
    {resume_text}
    
    The JSON format should include the following fields:
    - Name
    - Title
    - Education
    - Technical Skills
    - Work Experience
    - Certifications
    - Projects
    
    Please provide the JSON output.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except openai.error.APIConnectionError as e:
        print("The server could not be reached.")
        print(e.__cause__)  # An underlying Exception, likely raised within httpx.
    except openai.error.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except openai.error.APIError as e:
        print("Another non-200-range status code was received.")
        print(e.status_code)
        print(e.response)

# Function to select a file
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select Resume File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    return file_path

# Main script execution
if __name__ == "__main__":
    file_path = select_file()
    if file_path:
        try:
            with open(file_path, 'r') as file:
                resume_text = file.read()
            parsed_json = parse_resume_to_json(resume_text)
            print(parsed_json)
        except FileNotFoundError:
            print("The selected file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No file selected.")
