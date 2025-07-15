FROM mcr.microsoft.com/vscode/devcontainers/python:3

WORKDIR /usr/src/app

COPY . .
COPY . /usr/src/app
RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["python", "app.py"]
