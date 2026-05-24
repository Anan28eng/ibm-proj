# Hackathon Demo Checklist

## Pre-Demo Setup (15 minutes before)

### Backend Setup
- [ ] GEMINI_API_KEY environment variable is set
- [ ] Backend server is running: `python -m uvicorn main:app --reload`
- [ ] Backend accessible at http://localhost:8000
- [ ] Swagger docs working at http://localhost:8000/docs
- [ ] No startup errors in terminal

### Frontend Setup
- [ ] Frontend server is running: `npm run dev`
- [ ] Frontend accessible at http://localhost:3000
- [ ] Page loads without JavaScript errors
- [ ] All animations visible and smooth

### Browser Check
- [ ] Using Chrome, Firefox, or Edge
- [ ] Console shows no critical errors
- [ ] Network tab shows requests going to http://localhost:8000

## Demo Flow Verification

### Landing Page
- [ ] Hero section displays properly
- [ ] "Start Building" button is clickable
- [ ] Typewriter animation works
- [ ] Scroll animations trigger

### Dashboard Launch
- [ ] Dashboard loads after clicking "Start Building"
- [ ] Loading screen animation plays
- [ ] Pipeline visualization shows
- [ ] All 5 agent names visible in sidebar

### Idea Input
- [ ] Input field accepts text
- [ ] "Orchestrate →" button is enabled
- [ ] Example text: "AI-powered task management for engineering teams"

### Orchestration Execution
- [ ] Progress bar increments smoothly
- [ ] Terminal output displays in real-time
- [ ] Tabs unlock sequentially:
  - [ ] Validation tab (green) ✓
  - [ ] Architecture tab (blue) ✓
  - [ ] Code tab (purple) ✓
  - [ ] Security tab (amber) ✓
  - [ ] GitHub PR tab (red) ✓
- [ ] Each tab shows content when unlocked
- [ ] Status indicator: ORCHESTRATING → COMPLETE
- [ ] Overall progress reaches 100%

### Tab Content Verification
- [ ] **Validation Tab**: Shows PMF scores and verdict
- [ ] **Architecture Tab**: Shows tech stack selections
- [ ] **Code Tab**: Shows file tree and sample code
- [ ] **Security Tab**: Shows OWASP audit results
- [ ] **GitHub Tab**: Shows PR details with Open PR button

### OpenPR Button (Critical)
- [ ] Button is visible in GitHub tab
- [ ] Button is enabled after orchestration completes
- [ ] Button opens http://github.com/Anan28eng/ibm-proj in new tab
- [ ] Does NOT open VS Code or incorrect page
- [ ] Button has hover effects

### Error Handling
- [ ] If backend offline: Shows error message in input area
- [ ] Error message says "Running in simulation mode"
- [ ] Orchestration still proceeds (graceful degradation)
- [ ] No JavaScript console errors

### Visuals & UX
- [ ] Dark theme (dark background with light text)
- [ ] IBM Blue accent color (#0ea5e9)
- [ ] Smooth animations throughout
- [ ] No layout shifts or jumping elements
- [ ] Responsive on laptop screen
- [ ] Terminal output is readable
- [ ] All colors have good contrast

## Critical Bug Fixes Applied

### Frontend Fixes ✓
- [x] Removed hardcoded VS Code URL
- [x] Added backend API integration
- [x] Implemented error handling
- [x] Added PR URL extraction
- [x] Fixed button safety checks

### Backend Ready ✓
- [x] CORS configured for frontend
- [x] /generate endpoint functional
- [x] Response structure correct
- [x] Error handling in place
- [x] Logging configured

## Performance Checklist

- [ ] First load: < 3 seconds
- [ ] Orchestration start: < 1 second
- [ ] Each agent execution: 5-10 seconds average
- [ ] Total pipeline: 30-40 seconds
- [ ] No memory leaks (check Task Manager)
- [ ] CPU usage stays < 80%

## Hackathon Demo Script

1. **Introduction (30 seconds)**
   - "This is AI Co-Founder, an MVP generation platform"
   - "Watch how AI agents collaborate to build a startup MVP"

2. **Landing Page (20 seconds)**
   - Scroll down to show features
   - Highlight 5-agent pipeline

3. **Enter Idea (30 seconds)**
   - Click "Launch Mission Control"
   - Wait for loading screen
   - Paste startup idea: "AI-powered task management for engineering teams"

4. **Execute Pipeline (2 minutes)**
   - Click "Orchestrate →"
   - Narrate what's happening:
     - "Validation agent analyzing market fit... 20%"
     - "Architecture agent designing system... 40%"
     - "Builder agent generating code... 60%"
     - "Security agent reviewing... 80%"
     - "GitHub agent preparing PR... 100%"

5. **Showcase Results (1 minute)**
   - Click through each tab
   - Highlight key outputs
   - Show the PR button

6. **Critical Demo Moment**
   - Click "Open PR →"
   - Show GitHub repository opens in new tab
   - (Must NOT show VS Code page)
   - "This is where the generated MVP would be submitted"

## Backup Plan

If Backend Fails:
- Frontend shows error message but continues
- Terminal output still displays
- Tabs still populate with mock data
- OpenPR button opens default GitHub URL
- Demo continues smoothly

If Frontend Fails:
- Restart: `npm run dev`
- Clear browser cache
- Hard refresh (Ctrl+Shift+R)
- Open incognito window

If Both Fail:
- Have screenshots/video ready
- Show Swagger API docs instead
- Explain architecture and agents

## Post-Demo Cleanup

- [ ] Stop frontend server (Ctrl+C)
- [ ] Stop backend server (Ctrl+C)
- [ ] Close browser tabs
- [ ] Commit any demo artifacts
- [ ] Note any issues for future improvement

---

## Success Criteria for Judges

✅ **Functionality**
- Multi-agent system orchestrates correctly
- OpenPR button works perfectly
- Frontend-backend integration seamless

✅ **User Experience**
- Smooth animations and transitions
- Clear visual feedback on progress
- Professional design and polish

✅ **Innovation**
- Intelligent agent collaboration
- Real AI-powered MVP generation
- Practical startup tool

✅ **Demo Readiness**
- No crashes or errors
- Quick startup time
- Impressive visual presentation

---
**Status**: Ready for Hackathon Submission
**Last Verified**: [Current Date]
**Demo Duration**: ~5 minutes
