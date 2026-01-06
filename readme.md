# LLM Setup Repository

This repository contains a **reproducible local environment** for running and fine-tuning small open-weight LLMs:

- **Phi-3 Mini (3.8B)** – Microsoft  
- **Llama 3.2 — 3B** – Meta  
- **Gemma 2 — 2B** – Google  

You can prepare everything on a smaller laptop (CPU-only) and later move to a desktop with a powerful NVIDIA GPU for faster inference and fine-tuning.

---

## Repo Structure

```
llm-setup/
├─ docker/
│  ├─ ollama/           # Ollama inference container
│  │  ├─ Dockerfile
│  │  ├─ entrypoint.sh  # Optional auto-model-pull script
│  │  └─ ollama.yaml    # Ollama config (if needed)
│  └─ training/         # Fine-tuning container
│     ├─ Dockerfile
│     └─ requirements.txt
├─ compose.yaml          # Docker Compose orchestration
├─ README.md             # This file
└─ data/                 # Optional: datasets, logs, or fine-tuning data
```

## Running

Build and start

```bash
 docker compose up -d --build 
 ```

It should autopull the models, if not so then run:

```bash
docker exec -it ollama ollama pull phi3
docker exec -it ollama ollama pull llama3
docker exec -it ollama ollama pull gemma2
```

## Test

```bash 
docker exec -it ollama ollama run phi3
```

## Fine tuning (QLoRA/LoRA)

### Build training container

```bash 
docker build -t llm-training ./docker/training
```

### Run training container
```bash 
docker run --gpus all -it --rm \
  -v $(pwd)/data:/workspace/data \
  llm-training bash
```




## Notes

The entrypoint script can check if models already exist and skip pulling if they are cached.
All volumes are mounted to ./ollama for persistence.
Keep requirements.txt updated with any additional packages you may need for fine-tuning.
This setup is fully source-controlled, reproducible, and portable across machines.




