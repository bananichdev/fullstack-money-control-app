FROM python:3.12-alpine

RUN pip install poetry
WORKDIR /server/passport

COPY . .
RUN poetry install

EXPOSE 8000

CMD poetry run alembic upgrade head && poetry run uvicorn main:app --host 0.0.0.0 --port 8000
