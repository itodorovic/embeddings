# Embeddings Application

This application is a FastAPI server that provides an API for working with embeddings. It's built with Python and packaged with Docker for easy deployment and scaling.

## Features

- FastAPI for creating the web server and defining the API.
- Docker for packaging the application and its dependencies.
- AnglE for generating embeddings.

## Getting Started

To run this application, you need to have Docker installed on your machine. Once you have Docker, you can build and run the application with the following commands:

```bash
docker build -t embeddings:latest .
docker run -p 8080:8080 embeddings:latest
```

The application will be available at http://localhost:8080.

##API Endpoints

- GET /: Returns the model info, a message indicating the model is running, and information about the available routes.

- GET /health: Returns the health status of the application.

- POST /v1/embeddings: Returns embeddings for the input text. Usage: curl -H 'Content-Type: application/json' -d '{"input": "Your text string goes here"}' http://localhost:8080/v1/embeddings

## License

This project is licensed under the terms of the Apache 2.0 license.
