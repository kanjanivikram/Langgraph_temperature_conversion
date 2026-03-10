FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv sync

EXPOSE 8080
CMD ["uv", "run", "python", "app.py"]
