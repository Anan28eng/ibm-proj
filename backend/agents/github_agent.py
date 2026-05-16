"""
GitHub Workflow Agent
Prepares code for GitHub integration with PR templates and documentation.

This agent provides:
- Repository setup information
- Pull request templates and descriptions
- Commit message suggestions
- GitHub Actions workflow
- Documentation files
"""

import os
import json
from typing import Dict, List, Any, Optional
import google.generativeai as genai


def github_agent(
    idea: str,
    code_scaffold: Dict[str, Any],
    security_report: Optional[Dict[str, Any]] = None,
    architecture: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate GitHub integration package for the MVP.
    
    Args:
        idea (str): The startup idea description
        code_scaffold (Dict): Output from builder_agent
        security_report (Dict, optional): Output from security_agent
        architecture (Dict, optional): Output from architect_agent
        
    Returns:
        Dict containing:
            - repository_status: Repo setup information
            - pull_request_info: PR template and description
            - commit_summary: Suggested commit messages
            - github_actions: CI/CD workflow file
            - documentation: Additional docs (CONTRIBUTING, etc.)
            
    Example:
        >>> result = github_agent(idea, code_scaffold, security_report)
        >>> print(result['pull_request_info']['title'])
    """
    
    # Initialize Gemini client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Construct the prompt
    prompt = _build_prompt(idea, code_scaffold, security_report, architecture)
    
    try:
        # Call Gemini API
        system_instruction = "You are a DevOps expert specializing in GitHub workflows and documentation. Generate professional, comprehensive GitHub integration materials. Return only valid JSON."
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.5,
                max_output_tokens=2000
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
            "message": f"GitHub integration generation failed: {str(e)}",
            "repository_status": {},
            "pull_request_info": {},
            "commit_summary": [],
            "github_actions": "",
            "documentation": {}
        }


def _build_prompt(
    idea: str,
    code_scaffold: Dict[str, Any],
    security_report: Optional[Dict[str, Any]] = None,
    architecture: Optional[Dict[str, Any]] = None
) -> str:
    """
    Build the prompt for GitHub integration generation.
    
    Args:
        idea (str): The startup idea
        code_scaffold (Dict): Generated code
        security_report (Dict, optional): Security analysis
        architecture (Dict, optional): Technical architecture
        
    Returns:
        str: Formatted prompt
    """
    
    # Extract context
    files_count = len(code_scaffold.get("react_scaffold", {})) + len(code_scaffold.get("fastapi_scaffold", {}))
    
    security_context = ""
    if security_report and not security_report.get("error"):
        rating = security_report.get("security_rating", 0)
        severity = security_report.get("severity_summary", {})
        security_context = f"""
SECURITY ANALYSIS:
- Security Rating: {rating}/100
- Critical Issues: {severity.get('critical', 0)}
- High Issues: {severity.get('high', 0)}
- Total Issues: {sum(severity.values())}
"""
    
    tech_context = ""
    if architecture and not architecture.get("error"):
        frontend = architecture.get('frontend_stack', {})
        backend = architecture.get('backend_stack', {})
        tech_context = f"""
TECH STACK:
- Frontend: {frontend.get('framework', 'React')}
- Backend: {backend.get('framework', 'FastAPI')}
- Database: {architecture.get('database_schema', {}).get('database_type', 'PostgreSQL')}
"""
    
    prompt = f"""Generate a complete GitHub integration package for this MVP project:

PROJECT OVERVIEW:
{idea}

CODE SCAFFOLD:
- Total Files Generated: {files_count}
- Frontend Components: {len(code_scaffold.get('react_scaffold', {}))}
- Backend Files: {len(code_scaffold.get('fastapi_scaffold', {}))}
{tech_context}
{security_context}

Generate comprehensive GitHub integration materials:

1. REPOSITORY STATUS
   - Repository name suggestion
   - Description (1-2 sentences)
   - Topics/tags for discoverability
   - License recommendation
   - Repository visibility (public/private)
   - Branch strategy (main, develop, etc.)

2. PULL REQUEST INFO
   - PR Title (clear, descriptive)
   - PR Description with:
     * What was built
     * Key features (bullet points)
     * Technical decisions
     * Testing performed
     * Security considerations
     * Breaking changes (if any)
     * Screenshots/demos section
   - PR Labels (feature, enhancement, etc.)
   - Reviewers suggestions

3. COMMIT SUMMARY
   - 5-8 logical commit messages following conventional commits format
   - Group related changes
   - Format: type(scope): description
   - Types: feat, fix, docs, style, refactor, test, chore
   - Each commit should be atomic and meaningful

4. GITHUB ACTIONS WORKFLOW
   - Complete .github/workflows/ci.yml file
   - CI/CD pipeline with:
     * Linting and formatting
     * Unit tests
     * Security scanning
     * Build verification
     * Deployment (optional)
   - Trigger on push and PR
   - Use appropriate actions from marketplace

5. DOCUMENTATION FILES
   - CONTRIBUTING.md (how to contribute)
   - CODE_OF_CONDUCT.md (community guidelines)
   - CHANGELOG.md (version 0.1.0 initial release)
   - .github/ISSUE_TEMPLATE/bug_report.md
   - .github/ISSUE_TEMPLATE/feature_request.md
   - .github/PULL_REQUEST_TEMPLATE.md

OUTPUT FORMAT:
Return ONLY valid JSON matching this exact structure:
{{
  "repository_status": {{
    "name": "string",
    "description": "string",
    "topics": ["string"],
    "license": "MIT|Apache-2.0|GPL-3.0|etc",
    "visibility": "public|private",
    "branch_strategy": "string"
  }},
  "pull_request_info": {{
    "title": "string",
    "description": "string (markdown formatted)",
    "labels": ["string"],
    "reviewers": ["string"]
  }},
  "commit_summary": [
    {{
      "message": "string",
      "description": "string",
      "files_affected": ["string"]
    }}
  ],
  "github_actions": "string (complete YAML workflow file)",
  "documentation": {{
    "CONTRIBUTING.md": "string",
    "CODE_OF_CONDUCT.md": "string",
    "CHANGELOG.md": "string",
    "bug_report_template.md": "string",
    "feature_request_template.md": "string",
    "pull_request_template.md": "string"
  }}
}}

REQUIREMENTS:
- Professional, clear documentation
- Follow GitHub best practices
- Use conventional commits format
- Include security considerations
- Make it beginner-friendly
- Optimize for open-source collaboration

IMPORTANT:
- Use markdown formatting for documentation
- Include emojis for better readability
- Be specific and actionable
- Consider MVP/hackathon context
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
        "repository_status": raw_result.get("repository_status", {}),
        "pull_request_info": raw_result.get("pull_request_info", {}),
        "commit_summary": raw_result.get("commit_summary", []),
        "github_actions": raw_result.get("github_actions", ""),
        "documentation": raw_result.get("documentation", {}),
        "error": False
    }
    
    # Ensure dicts are actually dicts
    if not isinstance(structured["repository_status"], dict):
        structured["repository_status"] = {}
    
    if not isinstance(structured["pull_request_info"], dict):
        structured["pull_request_info"] = {}
    
    if not isinstance(structured["documentation"], dict):
        structured["documentation"] = {}
    
    # Ensure lists are actually lists
    if not isinstance(structured["commit_summary"], list):
        structured["commit_summary"] = []
    
    # Ensure strings are actually strings
    if not isinstance(structured["github_actions"], str):
        structured["github_actions"] = ""
    
    return structured


def save_github_files(result: Dict[str, Any], output_dir: str = "./generated_mvp") -> Dict[str, str]:
    """
    Save GitHub integration files to disk.
    
    Args:
        result (Dict): Output from github_agent()
        output_dir (str): Base directory for the project
        
    Returns:
        Dict: Mapping of file paths to status
    """
    import os
    
    if result.get("error"):
        return {"error": result.get("message", "Unknown error")}
    
    saved_files = {}
    
    try:
        # Create .github directory structure
        github_dir = os.path.join(output_dir, ".github")
        workflows_dir = os.path.join(github_dir, "workflows")
        issue_templates_dir = os.path.join(github_dir, "ISSUE_TEMPLATE")
        
        os.makedirs(workflows_dir, exist_ok=True)
        os.makedirs(issue_templates_dir, exist_ok=True)
        
        # Save GitHub Actions workflow
        workflow_path = os.path.join(workflows_dir, "ci.yml")
        with open(workflow_path, 'w', encoding='utf-8') as f:
            f.write(result.get("github_actions", ""))
        saved_files[workflow_path] = "saved"
        
        # Save documentation files
        docs = result.get("documentation", {})
        
        # Root level docs
        for filename in ["CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "CHANGELOG.md"]:
            if filename in docs:
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(docs[filename])
                saved_files[filepath] = "saved"
        
        # Issue templates
        if "bug_report_template.md" in docs:
            filepath = os.path.join(issue_templates_dir, "bug_report.md")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(docs["bug_report_template.md"])
            saved_files[filepath] = "saved"
        
        if "feature_request_template.md" in docs:
            filepath = os.path.join(issue_templates_dir, "feature_request.md")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(docs["feature_request_template.md"])
            saved_files[filepath] = "saved"
        
        # PR template
        if "pull_request_template.md" in docs:
            filepath = os.path.join(github_dir, "PULL_REQUEST_TEMPLATE.md")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(docs["pull_request_template.md"])
            saved_files[filepath] = "saved"
        
        return saved_files
        
    except Exception as e:
        return {"error": f"Failed to save GitHub files: {str(e)}"}


def get_github_summary(result: Dict[str, Any]) -> str:
    """
    Generate a human-readable summary of GitHub integration.
    
    Args:
        result (Dict): Output from github_agent()
        
    Returns:
        str: Formatted summary
    """
    if result.get("error"):
        return f"Error: {result.get('message', 'Unknown error')}"
    
    repo = result.get("repository_status", {})
    pr = result.get("pull_request_info", {})
    commits = result.get("commit_summary", [])
    
    summary = f"""
GITHUB INTEGRATION SUMMARY
==========================

REPOSITORY:
- Name: {repo.get('name', 'N/A')}
- Description: {repo.get('description', 'N/A')}
- License: {repo.get('license', 'N/A')}
- Visibility: {repo.get('visibility', 'N/A')}
- Topics: {', '.join(repo.get('topics', []))}

PULL REQUEST:
- Title: {pr.get('title', 'N/A')}
- Labels: {', '.join(pr.get('labels', []))}

COMMITS:
- Total Commits: {len(commits)}
"""
    
    if commits:
        summary += "\nCommit Messages:\n"
        for i, commit in enumerate(commits[:5], 1):
            summary += f"{i}. {commit.get('message', 'N/A')}\n"
    
    summary += f"\nDOCUMENTATION FILES:"
    docs = result.get("documentation", {})
    summary += f"\n- Files Generated: {len(docs)}"
    
    summary += f"\n\nCI/CD WORKFLOW:"
    workflow = result.get("github_actions", "")
    summary += f"\n- Workflow File: {'✓ Generated' if workflow else '✗ Missing'}"
    
    return summary


def get_pr_description(result: Dict[str, Any]) -> str:
    """
    Get the formatted PR description.
    
    Args:
        result (Dict): Output from github_agent()
        
    Returns:
        str: PR description in markdown
    """
    if result.get("error"):
        return f"Error: {result.get('message', 'Unknown error')}"
    
    pr = result.get("pull_request_info", {})
    return pr.get("description", "No PR description available")


def get_commit_messages(result: Dict[str, Any]) -> List[str]:
    """
    Get list of commit messages.
    
    Args:
        result (Dict): Output from github_agent()
        
    Returns:
        List[str]: Commit messages
    """
    if result.get("error"):
        return []
    
    commits = result.get("commit_summary", [])
    return [commit.get("message", "") for commit in commits]


# Example usage and testing
if __name__ == "__main__":
    # Test with sample data
    test_idea = """
    A mobile app that helps busy professionals track their daily water intake.
    Users set hydration goals, receive smart reminders based on their activity level,
    and can compete with friends.
    """
    
    test_scaffold = {
        "react_scaffold": {
            "App.jsx": "...",
            "components/HomePage.jsx": "...",
            "components/Dashboard.jsx": "..."
        },
        "fastapi_scaffold": {
            "main.py": "...",
            "models.py": "...",
            "routes.py": "..."
        }
    }
    
    test_security = {
        "security_rating": 85,
        "severity_summary": {
            "critical": 0,
            "high": 1,
            "medium": 3,
            "low": 2
        }
    }
    
    test_architecture = {
        "frontend_stack": {
            "framework": "React"
        },
        "backend_stack": {
            "framework": "FastAPI"
        },
        "database_schema": {
            "database_type": "PostgreSQL"
        }
    }
    
    print("Generating GitHub integration package...")
    print("=" * 50)
    
    result = github_agent(test_idea, test_scaffold, test_security, test_architecture)
    
    if result.get("error"):
        print(f"Error: {result.get('message')}")
    else:
        print(get_github_summary(result))
        
        print("\n" + "=" * 50)
        print("PULL REQUEST DESCRIPTION:")
        print(get_pr_description(result))
        
        print("\n" + "=" * 50)
        print("COMMIT MESSAGES:")
        for i, msg in enumerate(get_commit_messages(result), 1):
            print(f"{i}. {msg}")
        
        print("\n" + "=" * 50)
        print("GITHUB ACTIONS WORKFLOW (first 500 chars):")
        print(result.get("github_actions", "")[:500])
        
        # Save files
        print("\n" + "=" * 50)
        print("Saving GitHub files...")
        saved = save_github_files(result, "./test_mvp")
        if "error" in saved:
            print(f"Error saving: {saved['error']}")
        else:
            print(f"Successfully saved {len(saved)} files!")
            for filepath in saved.keys():
                print(f"  ✓ {filepath}")
        
        # Print full JSON for debugging
        print("\n" + "=" * 50)
        print("FULL JSON OUTPUT:")
        print(json.dumps(result, indent=2))

# Made with Bob
