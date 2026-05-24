# AI Co-Founder - Hackathon Deployment Guide

## Quick Start (5 minutes)

### Prerequisites
- Python 3.9+
- Node.js 18+
- GEMINI_API_KEY environment variable set

### Step 1: Set Environment Variable
```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your-api-key-here"

# Windows CMD
set GEMINI_API_KEY=your-api-key-here

# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"
```

### Step 2: Start Backend (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
# Backend will run on http://localhost:8000
# Swagger docs available at http://localhost:8000/docs
```

### Step 3: Start Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
# Frontend will run on http://localhost:3000
```

### Step 4: Use the Application
1. Open http://localhost:3000 in your browser
2. Click "Start Building" or "Launch Mission Control"
3. Enter a startup idea (e.g., "AI-powered task management for remote teams")
4. Click "Orchestrate →"
5. Watch the pipeline execute through all 5 agents
6. Click "Open PR →" to view the GitHub repository link

## Demo Flow

1. **Validation**: Business feasibility analysis
2. **Architecture**: Technical stack design
3. **Code Gen**: MVP code scaffold generation
4. **Security**: OWASP security audit
5. **GitHub PR**: Pull request workflow simulation

## Key Features Fixed

✓ OpenPR button now opens valid GitHub repository
✓ Frontend-backend API integration functional
✓ Error handling with fallback modes
✓ Real API responses from orchestrator pipeline
✓ Professional UI with animations

## Troubleshooting

### Backend Connection Error
- Ensure backend is running on http://localhost:8000
- Check GEMINI_API_KEY is set correctly
- Look for error messages in backend console

### Slow Response
- First request may take 10-30 seconds (LLM inference)
- Subsequent requests will be faster
- Check your internet connection for Gemini API calls

### API Key Error
```
GEMINI_API_KEY environment variable not set
```
Solution: Set the environment variable before starting the backend

## File Structure
```
AI-Cofounder/
├── frontend/          # Next.js + React dashboard
│   ├── app/
│   │   ├── page.tsx   # Main dashboard & landing page
│   │   └── layout.tsx
│   ├── package.json
│   └── next.config.ts
├── backend/           # FastAPI orchestrator
│   ├── main.py        # FastAPI server
│   ├── orchestrator.py # Pipeline coordinator
│   ├── agents/        # AI agents
│   │   ├── business_agent.py
│   │   ├── architect_agent.py
│   │   ├── builder_agent.py
│   │   ├── security_agent.py
│   │   └── github_agent.py
│   └── requirements.txt
└── README.md
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│         Frontend (Next.js + React)                   │
│         http://localhost:3000                        │
└────────────────────┬────────────────────────────────┘
                     │ POST /generate
                     │
┌────────────────────▼────────────────────────────────┐
│         Backend (FastAPI)                            │
│         http://localhost:8000                        │
└────────────────────┬────────────────────────────────┘
                     │
           ┌─────────┴──────────┬──────────┬──────────┐
           │                    │          │          │
      ┌────▼────┐      ┌───────▼───┐ ┌───▼────┐ ┌───▼────┐
      │ Business│      │Architect  │ │Builder │ │Security│
      │ Agent   │      │Agent      │ │Agent   │ │Agent   │
      └────┬────┘      └───────┬───┘ └───┬────┘ └───┬────┘
           │                    │          │          │
           └─────────┬──────────┴──────────┴──────────┘
                     │
              ┌──────▼──────┐
              │ GitHub Agent│
              └──────┬──────┘
                     │
            ┌────────▼────────┐
            │ Orchestrator    │
            │ (Response Merge)│
            └────────┬────────┘
                     │
              ┌──────▼───────┐
              │ JSON Response │
              │ with PR Info  │
              └───────────────┘
```

## Production Notes

For production deployment:
- Set CORS origins appropriately (not "*")
- Use environment variables for configuration
- Add database persistence if needed
- Implement rate limiting
- Add authentication/authorization
- Use container orchestration (Docker/Kubernetes)

## Support

For issues:
1. Check backend logs on http://localhost:8000/docs
2. Verify GEMINI_API_KEY is valid
3. Check that both frontend and backend are running
4. Review error messages in browser console

---
Last Updated: Hackathon Submission
Status: Production-Ready for Demo
