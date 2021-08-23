FROM python:3.9 as builder

SHELL ["/bin/bash", "-xeuo", "pipefail", "-c"]

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - && ln -s "$HOME/.poetry/bin/poetry" /usr/local/bin/poetry && mkdir -p /opt/build

# Copy over the dependencies, pyproject.toml, and poetry.lock over
WORKDIR /opt/build
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes

# Copy the application code over.
WORKDIR /opt/app/
COPY . /opt/app/

FROM python:3.9

# pip install the generated requirements.txt file
COPY --from=builder /opt/build/ /opt/build/

RUN set -eux && pip3 install --no-cache-dir -r /opt/build/requirements.txt && rm -rf /opt/build ~/.cache/pip

# Copy the application code over
WORKDIR /opt/app/
COPY --from=builder /opt/app /opt/app/

ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "--use-colors" ]
CMD [ "garconne.main:app" ]

HEALTHCHECK --interval=1m --timeout=3s CMD curl -sfI http://localhost:8000/health || exit 1
