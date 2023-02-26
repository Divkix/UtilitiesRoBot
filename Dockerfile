FROM ghcr.io/divkix/docker-python-base:latest AS build
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /app
RUN apt update \
    && apt-get clean \
    && apt-get autoremove --purge --yes \
    && rm -rf /var/lib/apt/lists/* /root/* /tmp/* /var/cache/apt/archives/*.deb
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry export -f requirements.txt --without-hashes --output requirements.txt \
    && pip install --disable-pip-version-check -r requirements.txt
COPY . .
ENTRYPOINT ["python3"]
CMD ["-m", "bots"]
