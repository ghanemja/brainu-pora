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
COPY atp/    ./atp/
COPY graph/  ./graph/
COPY rag/    ./rag/
COPY eval/   ./eval/
COPY wiki/   ./wiki/
COPY data/   ./data/
COPY scripts/ ./scripts/

# Writable runtime dirs. HF Spaces runs the container as a non-root user, so
# the COPY'd (root-owned) /app/data must be world-writable for SQLite + the
# podcast/media cache. Harmless on Render/Fly (root there anyway).
RUN mkdir -p /app/data/sessions/media && chmod -R 777 /app/data
ENV BRAIN_DB=/app/data/brain_university.db

# Port: HF Spaces routes to app_port (7860); Render/Railway inject $PORT.
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=25s \
  CMD curl -fsS http://localhost:${PORT:-7860}/health || exit 1

CMD uvicorn api.server:app --host 0.0.0.0 --port ${PORT:-7860} --workers 1
