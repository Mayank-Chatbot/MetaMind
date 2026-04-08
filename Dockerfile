FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY meta_ai_env.py .
COPY index.html .
COPY openenv.yaml .

# Port 7860 for Hugging Face Spaces
EXPOSE 7860

CMD ["uvicorn", "meta_ai_env:app", "--host", "0.0.0.0", "--port", "7860"]
