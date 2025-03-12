---
title: QAModel
emoji: 👀
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: Demo project for  llm and fast api
---


Question-Answering (QA) API with FastAPI and Hugging Face
This project provides a FastAPI-based REST API for performing question-answering tasks using a pre-trained Hugging Face model. The API allows users to submit a context and a question, and it returns the answer extracted from the context.

Key Features
Lightweight Docker Image: Models are downloaded at runtime, keeping the Docker image small and efficient. #At the mooment supports a single model due to free hardware limitations on the HF spaces

Hugging Face Integration: Uses the transformers library to load and run pre-trained QA models.

Automated Model Download: Models are automatically downloaded and cached locally if they don't already exist.

Swagger Documentation: Interactive API documentation is available at /docs.

