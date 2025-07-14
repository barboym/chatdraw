FROM python:3.11-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["python", "app.py"]
