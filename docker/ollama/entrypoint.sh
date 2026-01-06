#!/usr/bin/env sh
set -e

echo "Starting Ollama…"
/bin/ollama serve &

# wait until server responds
until curl -s http://127.0.0.1:11434/api/tags >/dev/null; do
  echo "Waiting for Ollama to start…"
  sleep 2
done

echo "Pulling default models…"
ollama pull phi3
ollama pull llama3
ollama pull gemma2

echo "All models ready."
wait
