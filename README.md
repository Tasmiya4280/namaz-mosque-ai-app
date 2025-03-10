# Mosque-clock-ai

This FastAPI application allows users to upload recent time,time zone and an image of a clock displaying prayer times. The API processes the image using OpenAI's GPT-4o model to extract and return the prayer times in a structured JSON format.

## Clone the repository
```bash
git clone https://github.com/Shrhawk/mosque-clock-ai
```

## Navigate into the project directory
```bash
cd mosque-clock-ai
```

## Set Up Poetry

### Install Poetry (if not already installed)
```bash
pip install poetry
```

## Install Dependencies
```bash
poetry install
```

## Set Up Environment Variables

### Create a `.env` file and run this command to copy keys and after this add values against keys
```bash
cp sample_dotenv.txt .env
```

## Start the FastAPI Server
```bash
poetry run gunicorn --worker-class=uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

## API Usage

### Upload an Image

#### Endpoint
```
POST http://127.0.0.1:8000/upload-image/
```

#### Request
- Upload an image file of a clock displaying prayer times.

#### Example
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/upload-image/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@sample_image.jpeg' \
  -F 'time=12:00 PM' \
  -F 'timezone=UTC' \
  -F 'day=Sunday'
```

#### Example Response
```json
{
  "status": "success",
  "response": {
    "Fajar": "5:30 am",
    "Zohar": "1:30 pm",
    "Asar": "5:00 pm",
    "Maghrib": "6:27 pm",
    "Isha": "8:30 pm",
    "Jumma": "1:30 pm",
    "Next_Prayer": {
      "Prayer": "Zohar",
      "Time": "1:30 pm"
    }
  }
}
```

#### Swagger Docs

#### Example
```
  'http://127.0.0.1:8000/docs
```
