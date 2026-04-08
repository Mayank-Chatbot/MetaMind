from transformers import pipeline
import os

def init_model():
    """Initialize the text generation model"""
    model_name = os.getenv("MODEL_NAME", "google/flan-t5-small")
    return pipeline("text-generation", model=model_name)

def generate_response(task: str, model) -> str:
    """Generate a response for the given task"""
    try:
        # Use the model to generate a response
        result = model(task, max_length=200, num_return_sequences=1)
        return result[0]['generated_text']
    except Exception as e:
        return f"Error generating response: {str(e)}"

if __name__ == "__main__":
    # For testing
    model = init_model()
    test_task = "Explain how neural networks work"
    response = generate_response(test_task, model)
    print(f"Task: {test_task}")
    print(f"Response: {response}")
