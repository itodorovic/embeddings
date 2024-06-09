import os
from fastapi import FastAPI
from typing import Union, List, Dict, Tuple, Optional
from pydantic import BaseModel, Field
from angle_emb import AnglE

class EmbeddingInput(BaseModel):
    input: Union[List[str], Tuple[str], List[Dict], str] = Field(..., description="The input to be encoded")
    model: Optional[str] = None
    encoding_format: Optional[str] = 'float'
    dimensions: Optional[int] = None
    user: Optional[str] = None

app = FastAPI()

# Get the model name and path from the environment variables
model_name = os.getenv('MODEL_NAME', default='WhereIsAI/UAE-Large-V1')
model_path = os.getenv('MODEL_PATH', default='models/WhereIsAI/UAE-Large-V1')

# Load the model
try:
    angle_model = AnglE.from_pretrained(model_path, pooling_strategy='cls').to('cpu')
except Exception as e:
    print(f"Failed to load model from path {model_path}. Error: {str(e)}")

@app.get("/")
def read_root():
    return {
        "model_name": model_name,
        "model_path": model_path,
        "message": "Model is up and running",
        "route_info": {
            "/": "Returns the model info",
            "/health": "Returns the health status of the application",
            "/v1/embeddings": 'POST route to get embeddings. Usage: curl -H "Content-Type: application/json" -d \'{ "input": "Your text string goes here" }\' http://localhost:8080/v1/embeddings'
        }
    }

@app.get("/health")
def health_check():
    return {"health": "ok"}

@app.post("/v1/embeddings")
def get_embeddings(embedding_input: EmbeddingInput):
    # # Check if the input is an empty string
    # if not embedding_input.input.strip():
    #     return {
    #         "object": "list",
    #         "data": [],
    #         "model": model_name,
    #         "usage": {"prompt_tokens": 0, "total_tokens": 0},
    #     }

    # Encode the input text using the model
    embeddings = angle_model.encode(embedding_input.input, embedding_size=embedding_input.dimensions)

    # Create a response format compatible with OpenAI's API
    response = {
        "object": "list",
        "data": [
            {"object": "embedding", "index": i, "embedding": emb.tolist()}
            for i, emb in enumerate(embeddings)
        ],
        "model": model_name,
        "usage": {"prompt_tokens": len(embedding_input.input), "total_tokens": len(embedding_input.input)},
    }

    return response