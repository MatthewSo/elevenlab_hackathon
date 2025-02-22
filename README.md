# elevenlab_hackathon
Hackathon Repo for Eleven Labs

# Placeholder initialization
pip install -r requirements.txt

## Run Mock Service
uvicorn service_entry:app --host 0.0.0.0 --port 8000

- http://localhost:8000/speaking_state_data_stream
- http://localhost:8000/spoken_language_data_stream

## Run Frontend
cd into the frontend directory

- npm install
- npm run dev
