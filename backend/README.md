# AI Driven Energy Savings for RAN - Backend

## Backend Features

- /chat to provide chat response from llm model selected
- /refresh Pull in Kepler Data and save it to feed the llm 

## Technologies Used

- Python
- Uvicorn
- transformers

## Prerequisites

- Docker for Openshift deployment | Podman for local run
- Environment Variables to be set:
```
MODEL_URL = Inference url for llm
MODEL_ACCESS_KEY = Access key for llm

PROM_URL = Thanos querier for kepler data
PROM_ACCESS_TOKEN = Access token for Kepler data
```

## Setup and Installation

1. Clone the repository:
   ```
   #HTTPS
   https://gitlab.consulting.redhat.com/ai-odyssey-2025/ai-driven-energy-savings-for-ran/ai-energy-savings.git

   cd demo-project/backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start the development server:
   ```
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:8000`


## Containerization
Building and Running the Docker Container:

Build the Docker Image:

```
docker build -t backend .
```
Run the Docker Container:

```
docker run -d -p 8000:8000 backend
```

Access the API: You can now access the backend at http://localhost:8000.

