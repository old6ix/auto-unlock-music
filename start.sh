#!/bin/bash

docker compose up --build \
  --abort-on-container-exit --exit-code-from main

docker compose down \
  --volumes
