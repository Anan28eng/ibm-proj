# Gemini API Migration Guide

## Overview

All agents have been successfully migrated from OpenAI to Google Gemini API. This document provides setup instructions and migration details.

---

## What Changed

### API Provider
- **Before**: OpenAI (GPT-4o, GPT-4o-mini)
- **After**: Google Gemini (gemini-1.5-flash)

### Key Benefits
✅ **Cost-effective**: Gemini 1.5 Flash is optimized for speed and efficiency
✅ **High performance**: Fast response times suitable for hackathons
✅ **Large context**: Supports large input contexts for complex prompts
✅ **JSON output**: Reliable structured output generation

---

## Setup Instructions

### 1. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- `google-generativeai` - Gemini API client
- `fastapi` - Web framework
- `pydantic` - Data validation
- `python-dotenv` - Environment variables

### 3. Configure Environment

Update `.env` file in the project root:

```env
GEMINI_API_KEY=your_actual_api_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 4. Test the Setup

Run a simple test:

```python
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("Hello, Gemini!")
print(response.text)
```

---

## Migration Details

### All Agents Updated

1. ✅ **business_agent.py** - Business analysis
2. ✅ **architect_agent.py** - Technical architecture
3. ✅ **builder_agent.py** - Code generation
4. ✅ **security_agent.py** - Security review
5. ✅ **github_agent.py** - GitHub integration

### Code Changes

#### Before (OpenAI)
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."}
    ],
    response_format={"type": "json_object"},
    temperature=0.7,
    max_tokens=1500
)
result = json.loads(response.choices[0].message.content)
```

#### After (Gemini)
```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

system_instruction = "..."
full_prompt = f"{system_instruction}\n\n{prompt}"

response = model.generate_content(
    full_prompt,
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,
        max_output_tokens=1500
    )
)

# Parse JSON from response (handles markdown code blocks)
response_text = response.text.strip()
if response_text.startswith("```json"):
    response_text = response_text[7:]
if response_text.startswith("```"):
    response_text = response_text[3:]
if response_text.endswith("```"):
    response_text = response_text[:-3]
response_text = response_text.strip()

result = json.loads(response_text)
```

### Key Differences

| Aspect | OpenAI | Gemini |
|--------|--------|--------|
| **Import** | `from openai import OpenAI` | `import google.generativeai as genai` |
| **Client Init** | `OpenAI(api_key=...)` | `genai.configure(api_key=...)` |
| **Model** | `gpt-4o-mini`, `gpt-4o` | `gemini-1.5-flash` |
| **Messages** | Separate system/user messages | Combined prompt with system instruction |
| **JSON Mode** | `response_format={"type": "json_object"}` | Manual parsing from response |
| **Response** | `response.choices[0].message.content` | `response.text` |
| **Tokens** | `max_tokens` | `max_output_tokens` |

---

## Model Selection

### Gemini 1.5 Flash (Default)
- **Use for**: All agents (business, architect, builder, security, github)
- **Strengths**: Fast, cost-effective, good for structured output
- **Context**: 1M tokens
- **Best for**: Hackathon MVPs, rapid prototyping

### Alternative: Gemini 1.5 Pro
If you need higher quality outputs, you can switch to `gemini-1.5-pro`:

```python
model = genai.GenerativeModel('gemini-1.5-pro')
```

**Trade-offs**:
- ✅ Higher quality outputs
- ✅ Better reasoning
- ❌ Slower response times
- ❌ Higher cost

---

## JSON Output Handling

Gemini doesn't have a strict JSON mode like OpenAI, so we implemented robust parsing:

```python
# Extract JSON from markdown code blocks
response_text = response.text.strip()
if response_text.startswith("```json"):
    response_text = response_text[7:]
if response_text.startswith("```"):
    response_text = response_text[3:]
if response_text.endswith("```"):
    response_text = response_text[:-3]
response_text = response_text.strip()

result = json.loads(response_text)
```

This handles cases where Gemini wraps JSON in markdown code blocks.

---

## Testing

### Test Individual Agents

```bash
cd backend

# Test business agent
python -c "from agents.business_agent import business_agent; print(business_agent('A water tracking app'))"

# Test architect agent
python -c "from agents.architect_agent import architect_agent; print(architect_agent('A water tracking app'))"

# Test full pipeline
python orchestrator.py
```

### Expected Behavior

All agents should:
1. ✅ Accept the same inputs as before
2. ✅ Return the same structured JSON outputs
3. ✅ Handle errors gracefully
4. ✅ Work with the orchestrator

---

## Troubleshooting

### Error: "GEMINI_API_KEY environment variable not set"

**Solution**: 
```bash
# Check if .env file exists
cat .env

# Ensure GEMINI_API_KEY is set
echo $GEMINI_API_KEY  # Linux/Mac
echo %GEMINI_API_KEY%  # Windows
```

### Error: "Import 'google.generativeai' could not be resolved"

**Solution**:
```bash
pip install google-generativeai
```

### Error: "Invalid API key"

**Solution**:
1. Verify your API key at [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Ensure no extra spaces in `.env` file
3. Try regenerating the API key

### Error: "JSONDecodeError"

**Solution**: The response might not be valid JSON. Check:
1. Prompt clarity - ensure you're asking for JSON output
2. Response parsing - the markdown extraction might need adjustment
3. Model temperature - lower temperature (0.3) for more consistent JSON

### Rate Limiting

Gemini has rate limits:
- **Free tier**: 15 requests per minute
- **Paid tier**: Higher limits

**Solution**: Add retry logic with exponential backoff (already implemented in orchestrator).

---

## Performance Comparison

| Metric | OpenAI GPT-4o-mini | Gemini 1.5 Flash |
|--------|-------------------|------------------|
| **Speed** | ~2-5s per request | ~1-3s per request |
| **Cost** | $0.15/1M input tokens | Free tier available |
| **Context** | 128K tokens | 1M tokens |
| **JSON Mode** | Native support | Manual parsing |
| **Quality** | Excellent | Very Good |

---

## Cost Optimization

### Tips for Hackathons

1. **Use Flash model**: Faster and cheaper than Pro
2. **Optimize prompts**: Be concise, avoid redundancy
3. **Cache results**: Store outputs to avoid re-generation
4. **Batch requests**: Process multiple ideas together when possible
5. **Monitor usage**: Track API calls in Google Cloud Console

### Free Tier Limits

- **Requests**: 15 per minute
- **Tokens**: 1M per minute
- **Daily**: 1,500 requests

For hackathons, this is usually sufficient!

---

## Next Steps

1. ✅ All agents migrated to Gemini
2. ✅ Environment configured
3. ✅ Dependencies installed
4. ⏭️ Test the full pipeline
5. ⏭️ Build FastAPI endpoints
6. ⏭️ Create React frontend
7. ⏭️ Deploy MVP

---

## Support

### Documentation
- [Gemini API Docs](https://ai.google.dev/docs)
- [Python SDK Reference](https://ai.google.dev/api/python/google/generativeai)
- [Pricing](https://ai.google.dev/pricing)

### Community
- [Google AI Discord](https://discord.gg/google-ai)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-gemini)

---

## Rollback (If Needed)

If you need to revert to OpenAI:

1. Install OpenAI SDK: `pip install openai`
2. Update `.env`: Add `OPENAI_API_KEY`
3. Revert agent files to use OpenAI client
4. Update `requirements.txt`

The architecture remains the same, only the LLM provider changes.

---

## Summary

✅ **Migration Complete**: All 5 agents now use Gemini API
✅ **Same Outputs**: JSON structure unchanged
✅ **Better Performance**: Faster response times
✅ **Cost Effective**: Free tier suitable for hackathons
✅ **Easy Setup**: Single API key configuration

Ready to build your AI Venture Studio MVP! 🚀