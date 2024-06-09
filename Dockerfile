# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Define the model name as a build argument
ARG MODEL_NAME=WhereIsAI/UAE-Large-V1

# Set the model name and path as environment variables
ENV MODEL_NAME=$MODEL_NAME
ENV MODEL_PATH=/models/${MODEL_NAME}
ENV TRANSFORMERS_CACHE=/.cache

# Create /.cache directory and make it writable
RUN mkdir /.cache && chmod 777 /.cache

# Install necessary Python packages
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install Git and Git LFS
RUN apt-get update && apt-get install -y git curl
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install git-lfs
RUN git lfs install

# Clone the model repository and download the large files
RUN git clone https://huggingface.co/${MODEL_NAME} /models/${MODEL_NAME}
RUN cd /models/${MODEL_NAME} && git lfs pull

# Remove the onnx directory to reduce image size
RUN rm -rf /models/${MODEL_NAME}/onnx

# Copy your FastAPI app and the start script into the container
COPY ./app /app
COPY start.sh /start.sh

# Change the permissions of the start script
RUN chmod +x /start.sh

# Set the working directory
WORKDIR /app

# Expose the FastAPI port
EXPOSE 8080

# Start the FastAPI server using the start script
CMD ["/start.sh"]
