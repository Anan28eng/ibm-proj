"""
Technical Architecture Agent
Designs system architecture and recommends technology stack for startup MVPs.

This agent provides:
- Frontend stack recommendations
- Backend stack recommendations
- Database schema design
- API structure and endpoints
- Architecture summary and rationale
"""

import os
import json
from typing import Dict, List, Any, Optional
import google.generativeai as genai


def architect_agent(idea: str, business_insights: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Design technical architecture for a startup idea.
    
    Args:
        idea (str): The startup idea description
        business_insights (Dict, optional): Output from business_agent for context
        
    Returns:
        Dict containing:
            - frontend_stack: Frontend technologies and libraries
            - backend_stack: Backend framework and tools
            - database_schema: Database design with tables/collections
            - api_structure: API endpoints and methods
            - architecture_summary: Overall architecture explanation
            
    Example:
        >>> result = architect_agent("A mobile app for tracking water intake")
        >>> print(result['frontend_stack']['framework'])
        'React Native'
    """
    
    # Initialize Gemini client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Construct the prompt
    prompt = _build_prompt(idea, business_insights)
    
    try:
        # Call Gemini API
        system_instruction = "You are a senior software architect specializing in MVP development. Design practical, scalable architectures optimized for rapid development. Return only valid JSON."
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2500
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
            "message": f"Architecture design failed: {str(e)}",
            "frontend_stack": {},
            "backend_stack": {},
            "database_schema": {},
            "api_structure": [],
            "architecture_summary": ""
        }


def _build_prompt(idea: str, business_insights: Optional[Dict[str, Any]] = None) -> str:
    """
    Build the prompt for architecture design.
    
    Args:
        idea (str): The startup idea
        business_insights (Dict, optional): Business context
        
    Returns:
        str: Formatted prompt
    """
    
    # Add business context if available
    context = ""
    if business_insights and not business_insights.get("error"):
        context = f"""
BUSINESS CONTEXT:
- Viability Score: {business_insights.get('viability_score', 'N/A')}/100
- Primary Revenue Model: {business_insights.get('monetization_strategy', {}).get('primary_model', 'N/A')}
- Target Audience: {len(business_insights.get('target_audience', []))} segments identified
"""
    
    prompt = f"""Design a complete technical architecture for this startup MVP:

STARTUP IDEA:
{idea}
{context}

Design a production-ready MVP architecture with the following components:

1. FRONTEND STACK
   - Framework (React, Vue, React Native, Flutter, etc.)
   - UI Library (Material-UI, Tailwind, Chakra, etc.)
   - State Management (Redux, Zustand, Context API, etc.)
   - Key Libraries (routing, forms, HTTP client, etc.)
   - Justification for choices

2. BACKEND STACK
   - Framework (FastAPI, Express, Django, Flask, etc.)
   - Language (Python, Node.js, Go, etc.)
   - Authentication (JWT, OAuth, Session-based, etc.)
   - Key Libraries (ORM, validation, etc.)
   - Justification for choices

3. DATABASE SCHEMA
   - Database Type (PostgreSQL, MongoDB, MySQL, etc.)
   - Core Tables/Collections (5-10 main entities)
   - For each entity:
     * Name
     * Key fields with data types
     * Relationships to other entities
     * Indexes needed

4. API STRUCTURE
   - API Style (REST, GraphQL, gRPC)
   - 10-15 core endpoints with:
     * HTTP Method (GET, POST, PUT, DELETE)
     * Endpoint path
     * Purpose/description
     * Request body (if applicable)
     * Response structure
     * Authentication required (yes/no)

5. ARCHITECTURE SUMMARY
   - Overall architecture pattern (monolith, microservices, serverless)
   - Why this architecture fits the MVP
   - Scalability considerations
   - Deployment recommendations
   - Estimated development time

REQUIREMENTS:
- MVP-focused (not over-engineered)
- Modern, maintainable technologies
- Easy to deploy and scale
- Cost-effective for early stage
- Beginner-friendly where possible

OUTPUT FORMAT:
Return ONLY valid JSON matching this exact structure:
{{
  "frontend_stack": {{
    "framework": "string",
    "ui_library": "string",
    "state_management": "string",
    "key_libraries": ["string"],
    "justification": "string"
  }},
  "backend_stack": {{
    "framework": "string",
    "language": "string",
    "authentication": "string",
    "key_libraries": ["string"],
    "justification": "string"
  }},
  "database_schema": {{
    "database_type": "string",
    "entities": [
      {{
        "name": "string",
        "fields": [
          {{
            "name": "string",
            "type": "string",
            "required": boolean,
            "description": "string"
          }}
        ],
        "relationships": ["string"],
        "indexes": ["string"]
      }}
    ]
  }},
  "api_structure": {{
    "api_style": "REST|GraphQL|gRPC",
    "base_url": "string",
    "endpoints": [
      {{
        "method": "GET|POST|PUT|DELETE|PATCH",
        "path": "string",
        "description": "string",
        "request_body": {{}},
        "response": {{}},
        "auth_required": boolean
      }}
    ]
  }},
  "architecture_summary": {{
    "pattern": "string",
    "rationale": "string",
    "scalability": "string",
    "deployment": "string",
    "estimated_dev_time": "string"
  }}
}}

IMPORTANT:
- Be specific with technology versions when relevant
- Focus on proven, stable technologies
- Consider team skill requirements
- Optimize for rapid MVP development
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
        "frontend_stack": raw_result.get("frontend_stack", {}),
        "backend_stack": raw_result.get("backend_stack", {}),
        "database_schema": raw_result.get("database_schema", {}),
        "api_structure": raw_result.get("api_structure", {}),
        "architecture_summary": raw_result.get("architecture_summary", {}),
        "error": False
    }
    
    # Ensure nested structures are dicts
    if not isinstance(structured["frontend_stack"], dict):
        structured["frontend_stack"] = {}
    
    if not isinstance(structured["backend_stack"], dict):
        structured["backend_stack"] = {}
    
    if not isinstance(structured["database_schema"], dict):
        structured["database_schema"] = {}
    
    if not isinstance(structured["api_structure"], dict):
        structured["api_structure"] = {}
    
    if not isinstance(structured["architecture_summary"], dict):
        structured["architecture_summary"] = {}
    
    # Ensure entities is a list
    if "database_schema" in structured:
        if "entities" not in structured["database_schema"]:
            structured["database_schema"]["entities"] = []
        elif not isinstance(structured["database_schema"]["entities"], list):
            structured["database_schema"]["entities"] = []
    
    # Ensure endpoints is a list
    if "api_structure" in structured:
        if "endpoints" not in structured["api_structure"]:
            structured["api_structure"]["endpoints"] = []
        elif not isinstance(structured["api_structure"]["endpoints"], list):
            structured["api_structure"]["endpoints"] = []
    
    return structured


def get_architecture_summary(result: Dict[str, Any]) -> str:
    """
    Generate a human-readable summary of the architecture.
    
    Args:
        result (Dict): Output from architect_agent()
        
    Returns:
        str: Formatted summary
    """
    if result.get("error"):
        return f"Error: {result.get('message', 'Unknown error')}"
    
    summary = """
TECHNICAL ARCHITECTURE SUMMARY
==============================
"""
    
    # Frontend Stack
    frontend = result.get('frontend_stack', {})
    summary += f"\nFRONTEND STACK:"
    summary += f"\n- Framework: {frontend.get('framework', 'N/A')}"
    summary += f"\n- UI Library: {frontend.get('ui_library', 'N/A')}"
    summary += f"\n- State Management: {frontend.get('state_management', 'N/A')}"
    
    # Backend Stack
    backend = result.get('backend_stack', {})
    summary += f"\n\nBACKEND STACK:"
    summary += f"\n- Framework: {backend.get('framework', 'N/A')}"
    summary += f"\n- Language: {backend.get('language', 'N/A')}"
    summary += f"\n- Authentication: {backend.get('authentication', 'N/A')}"
    
    # Database
    db = result.get('database_schema', {})
    summary += f"\n\nDATABASE:"
    summary += f"\n- Type: {db.get('database_type', 'N/A')}"
    summary += f"\n- Entities: {len(db.get('entities', []))}"
    
    # API
    api = result.get('api_structure', {})
    summary += f"\n\nAPI:"
    summary += f"\n- Style: {api.get('api_style', 'N/A')}"
    summary += f"\n- Endpoints: {len(api.get('endpoints', []))}"
    
    # Architecture Summary
    arch = result.get('architecture_summary', {})
    summary += f"\n\nARCHITECTURE:"
    summary += f"\n- Pattern: {arch.get('pattern', 'N/A')}"
    summary += f"\n- Estimated Dev Time: {arch.get('estimated_dev_time', 'N/A')}"
    summary += f"\n- Rationale: {arch.get('rationale', 'N/A')}"
    
    return summary


def generate_tech_stack_markdown(result: Dict[str, Any]) -> str:
    """
    Generate a markdown document of the tech stack for documentation.
    
    Args:
        result (Dict): Output from architect_agent()
        
    Returns:
        str: Markdown formatted tech stack documentation
    """
    if result.get("error"):
        return f"# Error\n\n{result.get('message', 'Unknown error')}"
    
    md = "# Technical Architecture\n\n"
    
    # Frontend
    frontend = result.get('frontend_stack', {})
    md += "## Frontend Stack\n\n"
    md += f"**Framework:** {frontend.get('framework', 'N/A')}\n\n"
    md += f"**UI Library:** {frontend.get('ui_library', 'N/A')}\n\n"
    md += f"**State Management:** {frontend.get('state_management', 'N/A')}\n\n"
    md += "**Key Libraries:**\n"
    for lib in frontend.get('key_libraries', []):
        md += f"- {lib}\n"
    md += f"\n**Justification:** {frontend.get('justification', 'N/A')}\n\n"
    
    # Backend
    backend = result.get('backend_stack', {})
    md += "## Backend Stack\n\n"
    md += f"**Framework:** {backend.get('framework', 'N/A')}\n\n"
    md += f"**Language:** {backend.get('language', 'N/A')}\n\n"
    md += f"**Authentication:** {backend.get('authentication', 'N/A')}\n\n"
    md += "**Key Libraries:**\n"
    for lib in backend.get('key_libraries', []):
        md += f"- {lib}\n"
    md += f"\n**Justification:** {backend.get('justification', 'N/A')}\n\n"
    
    # Database
    db = result.get('database_schema', {})
    md += "## Database Schema\n\n"
    md += f"**Database Type:** {db.get('database_type', 'N/A')}\n\n"
    md += "### Entities\n\n"
    for entity in db.get('entities', []):
        md += f"#### {entity.get('name', 'Unknown')}\n\n"
        md += "**Fields:**\n"
        for field in entity.get('fields', []):
            required = "✓" if field.get('required') else "○"
            md += f"- {required} `{field.get('name')}` ({field.get('type')}) - {field.get('description', '')}\n"
        if entity.get('relationships'):
            md += f"\n**Relationships:** {', '.join(entity.get('relationships', []))}\n"
        if entity.get('indexes'):
            md += f"\n**Indexes:** {', '.join(entity.get('indexes', []))}\n"
        md += "\n"
    
    # API
    api = result.get('api_structure', {})
    md += "## API Structure\n\n"
    md += f"**Style:** {api.get('api_style', 'N/A')}\n\n"
    md += f"**Base URL:** `{api.get('base_url', 'N/A')}`\n\n"
    md += "### Endpoints\n\n"
    for endpoint in api.get('endpoints', []):
        auth = "🔒" if endpoint.get('auth_required') else "🔓"
        md += f"#### {auth} `{endpoint.get('method')} {endpoint.get('path')}`\n\n"
        md += f"{endpoint.get('description', 'N/A')}\n\n"
    
    # Architecture Summary
    arch = result.get('architecture_summary', {})
    md += "## Architecture Summary\n\n"
    md += f"**Pattern:** {arch.get('pattern', 'N/A')}\n\n"
    md += f"**Rationale:** {arch.get('rationale', 'N/A')}\n\n"
    md += f"**Scalability:** {arch.get('scalability', 'N/A')}\n\n"
    md += f"**Deployment:** {arch.get('deployment', 'N/A')}\n\n"
    md += f"**Estimated Development Time:** {arch.get('estimated_dev_time', 'N/A')}\n"
    
    return md


# Example usage and testing
if __name__ == "__main__":
    # Test with a sample idea
    test_idea = """
    A mobile app that helps busy professionals track their daily water intake.
    Users set hydration goals, receive smart reminders based on their activity level,
    and can compete with friends. The app integrates with fitness trackers and
    provides personalized hydration recommendations based on weather and exercise.
    """
    
    # Optional: Include business insights for context
    test_business_insights = {
        "viability_score": 75,
        "monetization_strategy": {
            "primary_model": "Freemium with premium subscription"
        },
        "target_audience": [
            {"segment_name": "Fitness Enthusiasts"},
            {"segment_name": "Health-Conscious Professionals"}
        ]
    }
    
    print("Designing technical architecture...")
    print("=" * 50)
    
    result = architect_agent(test_idea, test_business_insights)
    
    if result.get("error"):
        print(f"Error: {result.get('message')}")
    else:
        print(f"\nFrontend: {result['frontend_stack'].get('framework', 'N/A')}")
        print(f"Backend: {result['backend_stack'].get('framework', 'N/A')}")
        print(f"Database: {result['database_schema'].get('database_type', 'N/A')}")
        print(f"API Endpoints: {len(result['api_structure'].get('endpoints', []))}")
        print(f"Database Entities: {len(result['database_schema'].get('entities', []))}")
        
        print("\n" + "=" * 50)
        print(get_architecture_summary(result))
        
        # Generate markdown documentation
        print("\n" + "=" * 50)
        print("MARKDOWN DOCUMENTATION:")
        print(generate_tech_stack_markdown(result))
        
        # Print full JSON for debugging
        print("\n" + "=" * 50)
        print("FULL JSON OUTPUT:")
        print(json.dumps(result, indent=2))

# Made with Bob
