# Brain University backend — FastAPI + graph engine + podcast/video render.
# Runs on Render / Railway / Fly / any container host.
#
# Local test:
#   docker build -t brain-u .
#   docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -p 8080:8080 brain-u

FROM python:3.11-slim

# ffmpeg → moviepy/podcast render; curl → healthcheck; git → optional deps
RUN apt-get update && apt-get install -y --no-install-recommends \
      ffmpeg curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend code + data the engine needs at runtime
COPY agents/ ./agents/
COPY api/    ./api/
COPY graph/  ./graph/
COPY rag/    ./rag/
COPY eval/   ./eval/
COPY wiki/   ./wiki/
COPY data/   ./data/
COPY scripts/ ./scripts/

# SQLite lives on a mounted disk in production so it survives redeploys
ENV BRAIN_DB=/data/brain_university.db
VOLUME /data

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
  CMD curl -fsS http://localhost:${PORT:-8080}/health || exit 1

# $PORT is provided by the host (Render/Railway). Default 8080 locally.
CMD uvicorn api.server:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1
