import os
import logging
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

# Set up logging
logger = logging.getLogger(__name__)

# Define the model directory
MODEL_DIR = Path(__file__).parent.parent / "_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

# Hugging Face authentication token (from environment variable)
AUTH_TOKEN = os.getenv("auth_token")
if not AUTH_TOKEN:
    raise ValueError("Hugging Face auth_token environment variable is not set.")

class DataLocation(BaseModel):
    """
    Represents the location of a model (local path and optional cloud URI).
    """
    local_path: str
    cloud_uri: Optional[str] = None

    def exists_or_download(self):
        """
        Check if the model exists locally. If not, download it from Hugging Face.
        """
        if not os.path.exists(self.local_path):
            if self.cloud_uri is not None:
                logger.warning(f"Downloading model from Hugging Face: {self.cloud_uri}")
                # Download from Hugging Face
                tokenizer = AutoTokenizer.from_pretrained(
                    self.cloud_uri, token=AUTH_TOKEN
                )
                model = AutoModelForQuestionAnswering.from_pretrained(
                    self.cloud_uri, token=AUTH_TOKEN
                )
                # Save the model and tokenizer locally
                tokenizer.save_pretrained(self.local_path)
                model.save_pretrained(self.local_path)
                logger.info(f"Model saved to: {self.local_path}")
            else:
                raise ValueError(f"Model not found locally and no cloud URI provided: {self.local_path}")
        return self.local_path

# Define the model location


class QAModel:
    def __init__(self,model_name,model_locaton):
        """
        Initialize the QA model and tokenizer.
        """
        self.model_name = model_name
        self.model_location = model_locaton
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_model()  # Call the method to load the model and tokenizer

    def _load_model(self):
        """
        Load the tokenizer and model.
        """
        # Ensure the model is downloaded
        model_path = self.model_location.exists_or_download()

        # Load the tokenizer and model from the local path
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_path, return_dict=True).to(self.device)
        logger.info(f"Loaded QA model: {self.model_name}")

    def inference_qa(self, context: str, question: str):
        """
        Perform question-answering inference.
        Args:
            context (str): The text passage or document.
            question (str): The question to be answered.
        Returns:
            str: The predicted answer.
        """
        if self.tokenizer is None or self.model is None:
            raise ValueError("Model or tokenizer is not loaded.")

        # Tokenize inputs
        inputs = self.tokenizer(question, context, return_tensors="pt", truncation=True, padding=True)
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        # Perform inference
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Extract answer
        answer_start_index = outputs.start_logits.argmax()
        answer_end_index = outputs.end_logits.argmax()
        predict_answer_tokens = inputs["input_ids"][0, answer_start_index : answer_end_index + 1]
        answer = self.tokenizer.decode(predict_answer_tokens, skip_special_tokens=True)

        return answer



def load_qa_pipeline(model_name: str = "Gowtham122/albertqa"):
    """
    Load the QA model and tokenizer.
    """
    model_location = DataLocation(
        local_path=str(MODEL_DIR / model_name.replace("/", "-")),
        cloud_uri=model_name,  # Hugging Face model ID
    )
    qa_model = QAModel(model_name,model_location)
    return qa_model

def inference_qa(qa_pipeline, context: str, question: str):
    """
    Perform QA inference using the loaded pipeline.
    """
    return qa_pipeline.inference_qa(context, question)
