FROM ubuntu:24.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends g++ python3 python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 runner

WORKDIR /app
COPY runner/requirements.txt .
RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt
COPY runner ./runner

USER runner
EXPOSE 8001
CMD ["uvicorn", "runner.main:app", "--host", "0.0.0.0", "--port", "8001"]
