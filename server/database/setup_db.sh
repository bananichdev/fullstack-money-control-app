#!/bin/bash

psql -U postgres <<-EOSQL
    CREATE DATABASE "money-control";
EOSQL

psql -U postgres -d "money-control" <<-EOSQL
    CREATE SCHEMA "products";
    CREATE SCHEMA "passport";
EOSQL
