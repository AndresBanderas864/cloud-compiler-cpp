FROM ubuntu:24.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends g++ coreutils \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 runner

USER runner
WORKDIR /workspace
