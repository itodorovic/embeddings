#!/bin/bash

# # Get the number of cores
# num_cores=$(nproc --all)

# # Calculate the number of Uvicorn workers
# num_workers=$((2 * num_cores + 1))

# # Set the WEB_CONCURRENCY environment variable
# export WEB_CONCURRENCY=$num_workers

# Start the FastAPI application
exec uvicorn app.app:app --host 0.0.0.0 --port 8080