# 🧠 Railway LLM Setup Guide

**Can you run an LLM on Railway? YES! Here are your options:**

---

## 🎯 Quick Answer

Railway **CAN** run smaller LLMs, but for production you'll want:
- **Option 1:** Local Ollama (FREE, runs on your machine)
- **Option 2:** Railway + Replicate API (FAST, pay-per-use)
- **Option 3:** Linode GPU server (POWERFUL, $1000/month for serious models)
- **Option 4:** Modal/RunPod (FLEXIBLE, pay only when running)

---

## ✅ Option 1: Local Ollama (RECOMMENDED - FREE!)

**What:** Run LLMs on YOUR computer, Railway connects via API

**Pros:**
- ✅ FREE (uses your GPU/CPU)
- ✅ Full control over models
- ✅ No API costs
- ✅ Privacy (data never leaves your machine)

**Cons:**
- ❌ Requires your computer running 24/7
- ❌ Limited by your hardware
- ❌ Slower than cloud GPUs

### Setup Ollama Locally:

```bash
# Install Ollama (Mac/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama2:7b       # 7B params (fast, 4GB RAM)
ollama pull llama2:13b      # 13B params (better, 8GB RAM)
ollama pull llama2:70b      # 70B params (best, 32GB RAM)
ollama pull mistral:7b      # Fast alternative
ollama pull codellama:13b   # Code-focused

# Run server (default port 11434)
ollama serve

# Test it
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Why is consciousness important?"
}'
```

### Connect Helix to Ollama:

**Already configured!** Just set env vars:

```bash
# Railway variables
railway variables set HELIX_LLM_PROVIDER=ollama
railway variables set OLLAMA_BASE_URL=http://your-ip:11434
railway variables set HELIX_LLM_MODEL=llama2:7b
```

**For local testing:**
```bash
export HELIX_LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434
export HELIX_LLM_MODEL=llama2:7b
```

---

## 🚀 Option 2: Railway + Replicate (EASY & FAST)

**What:** Railway app calls Replicate's GPU cloud for LLM inference

**Pros:**
- ✅ NO server management
- ✅ Pay only for actual usage
- ✅ Fast GPU inference
- ✅ Access to 1000+ models

**Cons:**
- ❌ Costs money ($0.0001-0.01 per token)
- ❌ API rate limits
- ❌ Data sent to Replicate

### Setup Replicate:

```bash
# Get API key from replicate.com
railway variables set REPLICATE_API_TOKEN=r8_...

# Install SDK
pip install replicate

# Update your Helix config
railway variables set HELIX_LLM_PROVIDER=replicate
railway variables set HELIX_LLM_MODEL=meta/llama-2-70b-chat
```

### Update `backend/llm_agent_engine.py`:

```python
# Add Replicate support
import replicate

class LLMProvider(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    OLLAMA = "ollama"
    REPLICATE = "replicate"  # NEW!
    CUSTOM = "custom"

# In your LLM call function:
if LLM_PROVIDER == "replicate":
    output = replicate.run(
        "meta/llama-2-70b-chat",
        input={"prompt": prompt, "max_tokens": 500}
    )
```

**Costs:** ~$0.50-5 per 1000 requests (depends on model size)

---

## 💪 Option 3: Linode GPU Server (BEAST MODE)

**What:** Rent a GPU server, run ANY model you want

**Pros:**
- ✅ Run 70B+ parameter models
- ✅ Full control
- ✅ Unlimited inference
- ✅ Fine-tune your own models

**Cons:**
- ❌ $1000-3000/month for serious GPUs
- ❌ You manage everything
- ❌ Overkill unless you're scaling BIG

### Linode GPU Options:

```
GPU Plan          | GPU           | RAM   | Price/month | Best For
------------------|---------------|-------|-------------|------------------
Dedicated 24 GB   | RTX 6000 Ada  | 128GB | $1,000     | 70B models
Dedicated 48 GB   | 2x RTX 6000   | 256GB | $2,000     | Fine-tuning
Dedicated 96 GB   | 4x RTX 6000   | 512GB | $4,000     | Research/training
```

### Setup Linode GPU:

```bash
# 1. Create Linode GPU instance
# 2. Install CUDA drivers
# 3. Install Ollama or vLLM

# On Linode server:
curl -fsSL https://ollama.com/install.sh | sh
ollama serve --host 0.0.0.0

# On Railway:
railway variables set OLLAMA_BASE_URL=http://your-linode-ip:11434
railway variables set HELIX_LLM_PROVIDER=ollama
railway variables set HELIX_LLM_MODEL=llama2:70b
```

**When to use Linode:**
- You're serving 1000+ users
- You need custom fine-tuned models
- You want 70B+ parameter models
- You hate API rate limits

---

## ⚡ Option 4: Modal / RunPod (RECOMMENDED FOR PRODUCTION)

**What:** Serverless GPUs - pay only when running

**Pros:**
- ✅ Auto-scaling
- ✅ Pay per second (not per month)
- ✅ Fast cold starts
- ✅ Easy deployment

**Cons:**
- ❌ Learning curve
- ❌ Costs more than Ollama (less than Linode)

### Modal Example:

```python
# modal_llm.py
import modal

stub = modal.Stub("helix-llm")

@stub.function(gpu="A100")
def generate_text(prompt: str):
    from transformers import pipeline

    generator = pipeline('text-generation', model='meta-llama/Llama-2-70b')
    return generator(prompt, max_length=500)

# Deploy
modal deploy modal_llm.py

# Call from Railway
import requests
response = requests.post("https://your-modal-url/generate", json={"prompt": "..."})
```

**Costs:** ~$1-2 per hour when running, $0 when idle

---

## 🤔 Which Should You Choose?

### For Development (FREE):
✅ **Local Ollama** - Run on your machine while coding

### For Production (Low Scale):
✅ **Replicate** - Easy, scalable, pay-per-use

### For Production (High Scale):
✅ **Modal/RunPod** - Auto-scaling serverless GPUs

### For Research/Training:
✅ **Linode GPU** - Rent dedicated hardware

---

## 🧠 Your Helix Already Supports All These!

Check `backend/llm_agent_engine.py`:
- ✅ Anthropic Claude
- ✅ OpenAI GPT
- ✅ Ollama (local/remote)
- ✅ Custom endpoints (add Replicate/Modal here!)

### Quick Config:

```bash
# Local Ollama
export HELIX_LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434
export HELIX_LLM_MODEL=llama2:7b

# Anthropic Claude
export HELIX_LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...
export HELIX_LLM_MODEL=claude-3-5-sonnet-20241022

# OpenAI
export HELIX_LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...
export HELIX_LLM_MODEL=gpt-4-turbo-preview
```

---

## 💡 My Recommendation

**Start with Local Ollama** for free development:
```bash
ollama pull llama2:7b
ollama serve
```

**Deploy with Replicate** for production:
```bash
pip install replicate
export REPLICATE_API_TOKEN=r8_...
```

**Upgrade to Modal** when you hit scale:
```bash
modal deploy helix_llm.py
```

**Only get Linode** if you're fine-tuning or serving 10K+ users.

---

## 🚢 Railway CAN Run Small Models

You CAN run tiny models directly on Railway, but it's not ideal:

```dockerfile
# Dockerfile
FROM python:3.11
RUN pip install transformers torch

# This works but is SLOW without GPU
# Railway doesn't have GPUs yet
```

**Verdict:** Don't run LLMs directly on Railway. Use it to orchestrate external LLM APIs (Replicate/Modal/Ollama).

---

## 🎯 TL;DR

- **FREE:** Local Ollama on your machine
- **EASY:** Replicate API ($0.001-0.01/request)
- **SCALE:** Modal serverless GPUs ($1-2/hour)
- **BEAST:** Linode dedicated GPU ($1000+/month)

**For Helix:** Start with Ollama locally, deploy with Replicate, scale with Modal.

**Railway's role:** Orchestrate your LLM calls, don't run the LLM itself.

🧠 **Your system already supports all of this!** Just set the env vars.
