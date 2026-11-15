#!/bin/bash
echo "=== Initializing Open-Interpreter Sandbox Environment ==="
echo "Container Working Directory: $(pwd)"
echo "Python Version: $(python3 --version)"
echo "Open-Interpreter Version: $(interpreter --version)"
echo "========================================================"

# Configure Ollama connection for Open-Interpreter
# export OPENAI_API_BASE="http://host.docker.internal:11434/v1"
# export OPENAI_API_BASE="http://localhost:11434/v1"
# export OPENAI_API_KEY="ollama"

# Configure Gemini
# export GEMINI_API_KEY=<"YOUR_API_KEY">
# alias irun_gemini="i -y --model gemini/gemini-3.5-flash-lite"


# Start Ollama server in the background inside the container
# ollama serve &
ollama serve > /tmp/ollama.log 2>&1 &

# Wait a few seconds for Ollama service to spin up
sleep 3

echo "=== Open-Interpreter Sandbox Initialized ==="
echo "Ollama API Base set to: $OPENAI_API_BASE"
echo "Ollama API KEY set to: $OPENAI_API_KEY"
echo "=========================================="

# Execute passed command (defaults to /bin/bash)
exec "$@"
