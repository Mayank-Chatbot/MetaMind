import os
import requests

# Environment variables for inference configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co")
MODEL_NAME = os.getenv("MODEL_NAME", "google/flan-t5-small")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

# Only HF_TOKEN should not have a default value.
# If LOCAL_IMAGE_NAME is provided, it can be used for docker-based inference.

def init_client():
    """Initialize the Hugging Face inference client configuration."""
    return {
        "api_base": API_BASE_URL.rstrip("/"),
        "model_name": MODEL_NAME,
        "headers": {
            **({"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}),
            "Content-Type": "application/json",
        },
        "local_image": LOCAL_IMAGE_NAME,
    }

def generate_response(task: str, client) -> str:
    """Generate a response for the given task using Hugging Face inference API."""
    if client["local_image"]:
        return f"LOCAL_IMAGE_NAME is set to {client['local_image']}. Use from_docker_image() logic here."

    url = f"{client['api_base']}/models/{client['model_name']}"
    payload = {
        "inputs": task,
        "options": {"use_cache": False, "wait_for_model": True},
    }

    try:
        response = requests.post(url, headers=client["headers"], json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and data:
            if isinstance(data[0], dict) and "generated_text" in data[0]:
                return data[0]["generated_text"]
            return str(data[0])

        return str(data)
    except requests.RequestException as exc:
        return f"Error generating response: {exc}"

if __name__ == "__main__":
    client = init_client()
    test_task = "Explain how neural networks work"
    response = generate_response(test_task, client)
    print(f"Task: {test_task}")
    print(f"Response: {response}")
