FROM python:3.11-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -e .

COPY . .

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","80"]
