FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir openenv-core openai

CMD ["uvicorn", "env.study_env:app", "--host", "0.0.0.0", "--port", "7860"]