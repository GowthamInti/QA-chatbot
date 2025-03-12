import logging
from contextlib import asynccontextmanager
import uvicorn
from app.config import CONFIG
from app.models import load_qa_pipeline, inference_qa  # Custom functions for loading and inference
from app.schemas import QAQuery, QAResponse  # Pydantic schema for QA input/output
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

logger = logging.getLogger(__file__)
logger.info("App opened")

# Global variable to hold the QA model
qa_model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global qa_model
    logger.info("Loading QA model")
    qa_model = load_qa_pipeline(CONFIG.qa_model_path)  # Load the QA model
    logger.info("QA model loaded")
    yield
    # Clean up the model and release resources
    qa_model = None
    logger.info("QA model unloaded")

app = FastAPI(lifespan=lifespan)

# Route for QA
@app.post("/qa", response_model=QAResponse)
async def question_answering(q: QAQuery):
    """
    Endpoint for question-answering.
    Accepts a context and a question, and returns the answer.
    """
    if qa_model is None:
        return JSONResponse(
            content={"error": "QA model is not loaded"},
            status_code=503,
        )

    # Perform inference
    answer = inference_qa(qa_model, context=q.context, question=q.question)
    return JSONResponse(content={"answer": answer})

# Health check route
@app.get(CONFIG.AIP_HEALTH_ROUTE, status_code=200)
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=CONFIG.AIP_HTTP_PORT, reload=CONFIG.DEBUG
    )