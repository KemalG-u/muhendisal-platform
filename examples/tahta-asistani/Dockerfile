# Multi-stage Dockerfile (Bolum 9.1 pattern)
FROM python:3.12-slim AS builder

WORKDIR /build
COPY pyproject.toml ./
RUN pip install --no-cache-dir --user -e ".[dev]" --target /install

FROM python:3.12-slim

RUN useradd -m -u 1000 app
WORKDIR /home/app

COPY --from=builder /install /home/app/.local/lib/python3.12/site-packages
COPY --chown=app:app app/ ./app/

USER app
ENV PYTHONPATH=/home/app \
    PATH=/home/app/.local/bin:$PATH

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
