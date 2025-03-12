# Template QAModel

## Project Structure
```
app/
├── __init__.py
├── config.py          # Configuration settings
├── models.py          # QA model loading and inference
├── schemas.py         # Pydantic schemas for input/output
└── main.py            # FastAPI application

_models/               # Directory for storing downloaded models
requirements.txt       # Python dependencies
Dockerfile             # Docker configuration
README.md              # Project documentation
```

## Template Question-Answering (QA) API with FastAPI and Hugging Face

This project provides a FastAPI-based REST API for performing question-answering tasks using a pre-trained Hugging Face model. The API allows users to submit a context and a question, and it returns the answer extracted from the context.

## Installation and Setup

### Clone the Repository
```sh
git clone https://github.com/GowthamInti/QA-chatbot.git
cd QA-chatbot
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Run the Application
```sh
python -m app.main
```

### Docker Setup
#### Build the Docker Image
```sh
docker build -t qa-api .
```

#### Run the Docker Container
```sh
docker run -p 7860:7860 --env-file .env qa-api
```

## Key Features
- **Model Support**: : Currently supports only the `AlbertForQuestionAnswering model`.

- **Lightweight Docker Image**: Models are downloaded at runtime, keeping the Docker image small and efficient. *(Currently supports a single model due to free hardware limitations on Hugging Face Spaces.)*
- **Hugging Face Integration**: Uses the `transformers` library to load and run pre-trained QA models.
- **Automated Model Download**: Models are automatically downloaded and cached locally if they don't already exist.
- **Swagger Documentation**: Interactive API documentation is available at `/docs`.

## API Documentation
Once the application is running, you can access the interactive API documentation by visiting:
```
http://localhost:7860/docs
```
This provides an easy way to test the API endpoints and understand how to interact with the service.


## Acknowledgements
None of this would have been possible without the hard work by the `HuggingFace` team in developing the `Transformers` library.
