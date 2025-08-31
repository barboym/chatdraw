FROM ghcr.io/astral-sh/uv:0.8.14-python3.11-bookworm-slim

WORKDIR /usr/src/app/draw_service
# should make UV install everything to the system Python
ARG UV_SYSTEM_PYTHON=1

COPY . .

RUN rm /bin/sh && ln -s /bin/bash /bin/sh &&  uv sync

COPY . .

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME

CMD ["uv","run","uvicorn","app:app","--host","0.0.0.0","--port","80"]


