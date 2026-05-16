"""
Code Builder Agent
Generates scaffolded MVP code for React frontend and FastAPI backend.

This agent provides:
- React component scaffold
- FastAPI backend scaffold
- README with setup instructions
- requirements.txt for dependencies
"""

import os
import json
from typing import Dict, List, Any, Optional
import google.generativeai as genai


def builder_agent(
    idea: str,
    architecture: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate scaffolded MVP code based on startup idea and architecture.
    
    Args:
        idea (str): The startup idea description
        architecture (Dict, optional): Output from architect_agent for context
        
    Returns:
        Dict containing:
            - react_scaffold: React component files
            - fastapi_scaffold: FastAPI backend files
            - readme: Setup and usage instructions
            - requirements: Python dependencies
            - package_json: Node.js dependencies
            
    Example:
        >>> result = builder_agent("A mobile app for tracking water intake")
        >>> print(result['react_scaffold']['App.jsx'])
    """
    
    # Initialize Gemini client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Construct the prompt
    prompt = _build_prompt(idea, architecture)
    
    try:
        # Call Gemini API
        system_instruction = "You are an expert full-stack developer. Generate clean, production-ready MVP code scaffolds. Focus on simplicity and best practices. Return only valid JSON."
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=4000
            )
        )
        
        # Parse response - extract JSON from markdown if needed
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        result = json.loads(response_text)
        
        # Validate and structure output
        structured_result = _structure_output(result)
        
        return structured_result
        
    except Exception as e:
        # Return error structure for graceful handling
        return {
            "error": True,
            "message": f"Code generation failed: {str(e)}",
            "react_scaffold": {},
            "fastapi_scaffold": {},
            "readme": "",
            "requirements": "",
            "package_json": {}
        }


def _build_prompt(idea: str, architecture: Optional[Dict[str, Any]] = None) -> str:
    """
    Build the prompt for code scaffold generation.
    
    Args:
        idea (str): The startup idea
        architecture (Dict, optional): Technical architecture context
        
    Returns:
        str: Formatted prompt
    """
    
    # Add architecture context if available
    context = ""
    if architecture and not architecture.get("error"):
        frontend = architecture.get('frontend_stack', {})
        backend = architecture.get('backend_stack', {})
        db = architecture.get('database_schema', {})
        
        context = f"""
TECHNICAL ARCHITECTURE:
- Frontend: {frontend.get('framework', 'React')}
- Backend: {backend.get('framework', 'FastAPI')}
- Database: {db.get('database_type', 'PostgreSQL')}
- API Endpoints: {len(architecture.get('api_structure', {}).get('endpoints', []))}
"""
    
    prompt = f"""Generate a complete MVP code scaffold for this startup idea:

STARTUP IDEA:
{idea}
{context}

Generate a lightweight, hackathon-ready MVP scaffold with the following structure:

1. REACT FRONTEND SCAFFOLD
   Generate these core files:
   
   a) App.jsx - Main application component
      - Basic routing setup
      - Layout structure
      - State management setup
   
   b) components/HomePage.jsx - Landing page
      - Hero section
      - Feature highlights
      - Call-to-action
   
   c) components/Dashboard.jsx - Main user interface
      - Core functionality UI
      - Data display
      - User interactions
   
   d) services/api.js - API client
      - Axios/fetch setup
      - API endpoint functions
      - Error handling
   
   e) App.css - Basic styling
      - Clean, modern design
      - Responsive layout
      - Component styles

2. FASTAPI BACKEND SCAFFOLD
   Generate these core files:
   
   a) main.py - FastAPI application
      - App initialization
      - CORS middleware
      - Health check endpoint
   
   b) models.py - Pydantic models
      - Request/response schemas
      - Data validation models
   
   c) routes.py - API endpoints
      - 5-8 core endpoints
      - CRUD operations
      - Business logic
   
   d) database.py - Database setup
      - Database connection
      - Session management
      - Basic ORM setup
   
   e) config.py - Configuration
      - Environment variables
      - Settings management

3. README.md
   - Project overview
   - Features list
   - Setup instructions (step-by-step)
   - Running the application
   - API documentation
   - Tech stack used

4. requirements.txt
   - FastAPI and dependencies
   - Database drivers
   - Authentication libraries
   - Other Python packages

5. package.json
   - React and dependencies
   - UI libraries
   - Development tools
   - Scripts for dev/build

REQUIREMENTS:
- MVP-focused (not over-engineered)
- Clean, readable code
- Proper error handling
- Comments for complex logic
- Follow best practices
- Ready to run with minimal setup

OUTPUT FORMAT:
Return ONLY valid JSON matching this exact structure:
{{
  "react_scaffold": {{
    "App.jsx": "complete file content",
    "components/HomePage.jsx": "complete file content",
    "components/Dashboard.jsx": "complete file content",
    "services/api.js": "complete file content",
    "App.css": "complete file content"
  }},
  "fastapi_scaffold": {{
    "main.py": "complete file content",
    "models.py": "complete file content",
    "routes.py": "complete file content",
    "database.py": "complete file content",
    "config.py": "complete file content"
  }},
  "readme": "complete README.md content",
  "requirements": "complete requirements.txt content",
  "package_json": {{
    "name": "string",
    "version": "0.1.0",
    "dependencies": {{}},
    "devDependencies": {{}},
    "scripts": {{}}
  }}
}}

IMPORTANT:
- Generate COMPLETE, runnable files
- Include all necessary imports
- Add proper error handling
- Use modern syntax and patterns
- Keep it simple and maintainable
- Return ONLY the JSON object, no additional text
"""
    return prompt


def _structure_output(raw_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and structure the LLM output into a consistent format.
    
    Args:
        raw_result (Dict): Raw JSON from LLM
        
    Returns:
        Dict: Structured and validated output
    """
    # Ensure all required fields exist with defaults
    structured = {
        "react_scaffold": raw_result.get("react_scaffold", {}),
        "fastapi_scaffold": raw_result.get("fastapi_scaffold", {}),
        "readme": raw_result.get("readme", ""),
        "requirements": raw_result.get("requirements", ""),
        "package_json": raw_result.get("package_json", {}),
        "error": False
    }
    
    # Ensure scaffolds are dicts
    if not isinstance(structured["react_scaffold"], dict):
        structured["react_scaffold"] = {}
    
    if not isinstance(structured["fastapi_scaffold"], dict):
        structured["fastapi_scaffold"] = {}
    
    if not isinstance(structured["package_json"], dict):
        structured["package_json"] = {}
    
    # Ensure strings
    if not isinstance(structured["readme"], str):
        structured["readme"] = ""
    
    if not isinstance(structured["requirements"], str):
        structured["requirements"] = ""
    
    return structured


def save_scaffold_to_disk(result: Dict[str, Any], output_dir: str = "./generated_mvp") -> Dict[str, str]:
    """
    Save the generated scaffold to disk.
    
    Args:
        result (Dict): Output from builder_agent()
        output_dir (str): Directory to save files
        
    Returns:
        Dict: Mapping of file paths to status
    """
    import os
    
    if result.get("error"):
        return {"error": result.get("message", "Unknown error")}
    
    saved_files = {}
    
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Create frontend directory
        frontend_dir = os.path.join(output_dir, "frontend", "src")
        os.makedirs(frontend_dir, exist_ok=True)
        os.makedirs(os.path.join(frontend_dir, "components"), exist_ok=True)
        os.makedirs(os.path.join(frontend_dir, "services"), exist_ok=True)
        
        # Save React files
        for filename, content in result.get("react_scaffold", {}).items():
            filepath = os.path.join(frontend_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            saved_files[filepath] = "saved"
        
        # Create backend directory
        backend_dir = os.path.join(output_dir, "backend")
        os.makedirs(backend_dir, exist_ok=True)
        
        # Save FastAPI files
        for filename, content in result.get("fastapi_scaffold", {}).items():
            filepath = os.path.join(backend_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            saved_files[filepath] = "saved"
        
        # Save README
        readme_path = os.path.join(output_dir, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(result.get("readme", ""))
        saved_files[readme_path] = "saved"
        
        # Save requirements.txt
        req_path = os.path.join(backend_dir, "requirements.txt")
        with open(req_path, 'w', encoding='utf-8') as f:
            f.write(result.get("requirements", ""))
        saved_files[req_path] = "saved"
        
        # Save package.json
        pkg_path = os.path.join(output_dir, "frontend", "package.json")
        with open(pkg_path, 'w', encoding='utf-8') as f:
            json.dump(result.get("package_json", {}), f, indent=2)
        saved_files[pkg_path] = "saved"
        
        return saved_files
        
    except Exception as e:
        return {"error": f"Failed to save files: {str(e)}"}


def get_file_tree(result: Dict[str, Any]) -> str:
    """
    Generate a visual file tree of the scaffold.
    
    Args:
        result (Dict): Output from builder_agent()
        
    Returns:
        str: ASCII file tree
    """
    if result.get("error"):
        return f"Error: {result.get('message', 'Unknown error')}"
    
    tree = """
generated_mvp/
├── README.md
├── frontend/
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       ├── components/
│       │   ├── HomePage.jsx
│       │   └── Dashboard.jsx
│       └── services/
│           └── api.js
└── backend/
    ├── requirements.txt
    ├── main.py
    ├── models.py
    ├── routes.py
    ├── database.py
    └── config.py
"""
    return tree


def get_setup_instructions(result: Dict[str, Any]) -> str:
    """
    Generate quick setup instructions.
    
    Args:
        result (Dict): Output from builder_agent()
        
    Returns:
        str: Setup instructions
    """
    if result.get("error"):
        return f"Error: {result.get('message', 'Unknown error')}"
    
    instructions = """
QUICK SETUP INSTRUCTIONS
========================

1. BACKEND SETUP:
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   uvicorn main:app --reload

2. FRONTEND SETUP (in new terminal):
   cd frontend
   npm install
   npm run dev

3. ACCESS APPLICATION:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. ENVIRONMENT VARIABLES:
   Create .env file in backend/ with:
   - DATABASE_URL=your_database_url
   - SECRET_KEY=your_secret_key
   - Any other required variables

For detailed instructions, see README.md
"""
    return instructions


def get_scaffold_summary(result: Dict[str, Any]) -> str:
    """
    Generate a summary of the generated scaffold.
    
    Args:
        result (Dict): Output from builder_agent()
        
    Returns:
        str: Summary text
    """
    if result.get("error"):
        return f"Error: {result.get('message', 'Unknown error')}"
    
    react_files = len(result.get("react_scaffold", {}))
    fastapi_files = len(result.get("fastapi_scaffold", {}))
    
    summary = f"""
CODE SCAFFOLD SUMMARY
====================

Generated Files:
- React Components: {react_files} files
- FastAPI Backend: {fastapi_files} files
- Documentation: README.md
- Dependencies: requirements.txt, package.json

Frontend Stack:
- React with modern hooks
- Component-based architecture
- API service layer
- Responsive styling

Backend Stack:
- FastAPI framework
- Pydantic models
- RESTful API design
- Database integration ready

Ready to run with minimal setup!
"""
    return summary


# Example usage and testing
if __name__ == "__main__":
    # Test with a sample idea
    test_idea = """
    A mobile app that helps busy professionals track their daily water intake.
    Users set hydration goals, receive smart reminders based on their activity level,
    and can compete with friends. The app integrates with fitness trackers and
    provides personalized hydration recommendations based on weather and exercise.
    """
    
    # Optional: Include architecture for context
    test_architecture = {
        "frontend_stack": {
            "framework": "React",
            "ui_library": "Tailwind CSS"
        },
        "backend_stack": {
            "framework": "FastAPI",
            "language": "Python"
        },
        "database_schema": {
            "database_type": "PostgreSQL"
        },
        "api_structure": {
            "endpoints": [
                {"method": "GET", "path": "/api/users"},
                {"method": "POST", "path": "/api/hydration"}
            ]
        }
    }
    
    print("Generating MVP code scaffold...")
    print("=" * 50)
    
    result = builder_agent(test_idea, test_architecture)
    
    if result.get("error"):
        print(f"Error: {result.get('message')}")
    else:
        print(get_scaffold_summary(result))
        print("\n" + "=" * 50)
        print("FILE TREE:")
        print(get_file_tree(result))
        print("\n" + "=" * 50)
        print(get_setup_instructions(result))
        
        # Optionally save to disk
        print("\n" + "=" * 50)
        print("Saving scaffold to disk...")
        saved = save_scaffold_to_disk(result, "./test_mvp")
        if "error" in saved:
            print(f"Error saving: {saved['error']}")
        else:
            print(f"Successfully saved {len(saved)} files!")
            for filepath in saved.keys():
                print(f"  ✓ {filepath}")
        
        # Print sample file content
        print("\n" + "=" * 50)
        print("SAMPLE: App.jsx (first 500 chars)")
        print(result['react_scaffold'].get('App.jsx', 'N/A')[:500])
        
        print("\n" + "=" * 50)
        print("SAMPLE: main.py (first 500 chars)")
        print(result['fastapi_scaffold'].get('main.py', 'N/A')[:500])

# Made with Bob
