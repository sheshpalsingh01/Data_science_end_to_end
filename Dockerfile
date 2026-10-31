FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY requirements-runtime.txt .
RUN python -m pip install --no-cache-dir --retries 10 --timeout 120 -r requirements-runtime.txt \
    && useradd --create-home --shell /usr/sbin/nologin app

COPY --chown=app:app . .

RUN mkdir -p /app/logs && chown app:app /app/logs

USER app

EXPOSE 8080

CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-8080} application:app"]