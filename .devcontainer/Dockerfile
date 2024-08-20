# See this page for customizing this dev container. For example, they have
# some already-provided ways of installing NodeJS if needed:
# https://github.com/devcontainers/images/tree/main/src/python
FROM mcr.microsoft.com/devcontainers/python:3.12
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp
COPY .devcontainer/.zshenv /home/vscode/
ENTRYPOINT [ "zsh" ]
