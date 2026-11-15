FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
#    python3-venv \
    curl \
    zstd \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# RUN python3 -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"
# Silence Ollama debug logs and prevent Python output buffering
ENV OLLAMA_DEBUG=0 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install Ollama binary inside container
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pin setuptools below v82 to retain pkg_resources compatibility & open-interpreter
# RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir --break-system-packages "setuptools<82.0.0" open-interpreter

# Creating working directory
WORKDIR /oi_root_dir

# Copy the bash script into the working directory and grant execution permissions
COPY entrypoint.sh /oi_root_dir/entrypoint.sh
RUN chmod +x /oi_root_dir/entrypoint.sh
# ENTRYPOINT ["/oi_root_dir/entrypoint.sh"]

CMD ["/bin/bash"]
