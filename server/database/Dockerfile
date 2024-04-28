FROM postgres:alpine

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

COPY ./setup_db.sh /docker-entrypoint-initdb.d/

EXPOSE 5432
