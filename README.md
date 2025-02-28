# Mosque-clock-ai

This FastAPI application allows users to upload an image of a clock displaying prayer times. The API processes the image using OpenAI's GPT-4o model to extract and return the prayer times in a structured JSON format.


## Clone the repository
```bash
git clone https://github.com/Shrhawk/mosque-clock-ai
```

## Navigate into the project directory
```bash
cd mosque-clock-ai
```

Set Up Virtual Environment

## Create a virtual environment
```bash
python -m venv env
```

## Activate the virtual environment (Linux/macOS)
```bash
source env/bin/activate
```

## Activate the virtual environment (Windows)
env\Scripts\activate


## Install required Python packages
```bash
pip install -r requirements.txt
```
Set Up Environment Variables

## Create a .env file and add your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env


## Start the FastAPI server
```bash
uvicorn main:app --reload
```

API Usage

Upload an Image

## Endpoint

POST /upload-image/

Request

- Upload an image file  of a clock displaying prayer times.

Example

```bash
'POST' \
  'http://127.0.0.1:8000/upload-image/'
```

Example Response

{
  "status": "success",
  "response": {
    "Fajar": "05:30 AM",
    "Zohar": "12:45 PM",
    "Asar": "04:15 PM",
    "Maghrib": "06:30 PM",
    "Isha": "08:00 PM",
    "Jumma": "01:15 PM"
  }
}


