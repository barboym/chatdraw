FROM python:3.11-slim

RUN apt-get update \
&& apt-get install -y --no-install-recommends git \
&& apt-get purge -y --auto-remove \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -e .

COPY . .

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME 
USER $USERNAME

CMD ["uvicorn","app:app","--host","0.0.0.0","--port","80"]
