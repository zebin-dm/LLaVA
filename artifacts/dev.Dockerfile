# Define base image.
FROM nvcr.io/nvidia/pytorch:23.10-py3
## Set non-interactive to prevent asking for user inputs blocking image creation.
ENV DEBIAN_FRONTEND=noninteractive
## Set timezone as it is required by some packages.
ENV TZ=Europe/Berlin
## CUDA Home, required to find CUDA in some packages.
ENV CUDA_HOME="/usr/local/cuda"
# Install required apt packages.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    curl \
    ffmpeg \
    git \
    sudo \
    vim-tiny \
    wget && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install packages.
RUN pip install --upgrade pip setuptools pathtools promise