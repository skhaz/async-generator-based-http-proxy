FROM python:3.10-slim AS base

ENV PATH /opt/venv/bin:$PATH
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

FROM base AS builder
WORKDIR /opt
RUN python -m venv venv
COPY requirements/common.txt requirements.txt
RUN pip install --no-cache-dir --upgrade --requirement requirements.txt

FROM base
WORKDIR /opt
COPY --from=builder /opt/venv venv
COPY app app

ARG PORT=3000
ENV PORT $PORT
EXPOSE $PORT

RUN useradd -r user
USER user
CMD exec uvicorn --host 0.0.0.0 --port $PORT app.main:app