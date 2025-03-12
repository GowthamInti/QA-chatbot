from pydantic import BaseModel, Field

class QAQuery(BaseModel):
    """
    Schema for the question-answering input.
    """
    context: str = Field(
        ...,
        example="The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower.",
        description="The text passage or document that contains the information needed to answer the question."
    )
    question: str = Field(
        ...,
        example="Who designed the Eiffel Tower?",
        description="The question to be answered based on the provided context."
    )

    class Config:
        schema_extra = {
            "example": {
                "context": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower.",
                "question": "Who designed the Eiffel Tower?"
            }
        }

class QAResponse(BaseModel):
    """
    Schema for the question-answering output.
    """
    answer: str = Field(
        ...,
        example="Gustave Eiffel",
        description="The answer to the question based on the provided context."
    )

    class Config:
        schema_extra = {
            "example": {
                "answer": "Gustave Eiffel"
            }
        }