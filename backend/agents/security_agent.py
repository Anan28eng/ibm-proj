"""
Security Review Agent
Analyzes generated code for security vulnerabilities and best practices.

This agent provides:
- Vulnerability detection
- Severity classification
- Remediation suggestions
- Overall security rating
"""

import os
import json
from typing import Dict, List, Any, Optional
import google.generativeai as genai


def security_agent(
    code_scaffold: Dict[str, Any],
    architecture: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Analyze code scaffold for security vulnerabilities.
    
    Args:
        code_scaffold (Dict): Output from builder_agent with generated code
        architecture (Dict, optional): Output from architect_agent for context
        
    Returns:
        Dict containing:
            - vulnerabilities: List of security issues found
            - severity_summary: Count by severity level
            - remediation_suggestions: Actionable fixes
            - security_rating: Score from 0-100
            - compliance_checklist: OWASP Top 10 compliance
            
    Example:
        >>> result = security_agent(code_scaffold)
        >>> print(result['security_rating'])
        85
    """
    
    # Initialize Gemini client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Construct the prompt
    prompt = _build_prompt(code_scaffold, architecture)
    
    try:
        # Call Gemini API
        system_instruction = "You are a security expert specializing in web application security. Analyze code for vulnerabilities following OWASP Top 10 guidelines. Return only valid JSON."
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
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
            "message": f"Security analysis failed: {str(e)}",
            "vulnerabilities": [],
            "severity_summary": {},
            "remediation_suggestions": [],
            "security_rating": 0,
            "compliance_checklist": {}
        }


def _build_prompt(
    code_scaffold: Dict[str, Any],
    architecture: Optional[Dict[str, Any]] = None
) -> str:
    """
    Build the prompt for security analysis.
    
    Args:
        code_scaffold (Dict): Generated code files
        architecture (Dict, optional): Technical architecture context
        
    Returns:
        str: Formatted prompt
    """
    
    # Extract code samples for analysis
    backend_code = code_scaffold.get("fastapi_scaffold", {})
    frontend_code = code_scaffold.get("react_scaffold", {})
    
    # Create code summary for analysis
    code_summary = "BACKEND CODE:\n"
    for filename, content in backend_code.items():
        code_summary += f"\n--- {filename} ---\n"
        code_summary += content[:1000] if len(content) > 1000 else content  # Limit length
    
    code_summary += "\n\nFRONTEND CODE:\n"
    for filename, content in frontend_code.items():
        code_summary += f"\n--- {filename} ---\n"
        code_summary += content[:800] if len(content) > 800 else content  # Limit length
    
    # Add architecture context if available
    context = ""
    if architecture and not architecture.get("error"):
        backend = architecture.get('backend_stack', {})
        context = f"""
ARCHITECTURE CONTEXT:
- Backend Framework: {backend.get('framework', 'N/A')}
- Authentication: {backend.get('authentication', 'N/A')}
- Database: {architecture.get('database_schema', {}).get('database_type', 'N/A')}
"""
    
    prompt = f"""Perform a comprehensive security analysis of this MVP code scaffold:

{context}

{code_summary}

Analyze the code for security vulnerabilities and best practices. Focus on:

1. AUTHENTICATION & AUTHORIZATION
   - Password handling and hashing
   - Session management
   - Token security (JWT, etc.)
   - Access control implementation
   - Authentication bypass risks

2. INPUT VALIDATION & INJECTION
   - SQL injection vulnerabilities
   - NoSQL injection risks
   - Command injection
   - XSS (Cross-Site Scripting)
   - Input sanitization
   - Output encoding

3. DATA PROTECTION
   - Sensitive data exposure
   - Encryption at rest and in transit
   - API key management
   - Environment variable usage
   - Secure data storage

4. API SECURITY
   - CORS configuration
   - Rate limiting
   - API authentication
   - Error message information leakage
   - HTTP security headers

5. CONFIGURATION & DEPLOYMENT
   - Debug mode settings
   - Secret key management
   - HTTPS enforcement
   - Security headers
   - Dependency vulnerabilities

6. FRONTEND SECURITY
   - XSS prevention
   - CSRF protection
   - Secure cookie handling
   - Client-side validation
   - Sensitive data in localStorage

For each vulnerability found, provide:
- Severity: CRITICAL, HIGH, MEDIUM, LOW
- Category: (e.g., "Injection", "Authentication", "Data Exposure")
- File and location
- Description of the issue
- Remediation steps

OUTPUT FORMAT:
Return ONLY valid JSON matching this exact structure:
{{
  "vulnerabilities": [
    {{
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "category": "string",
      "file": "string",
      "line": "string or null",
      "title": "string",
      "description": "string",
      "remediation": "string",
      "cwe_id": "string or null"
    }}
  ],
  "severity_summary": {{
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0
  }},
  "remediation_suggestions": [
    "string"
  ],
  "security_rating": 0-100,
  "rating_justification": "string",
  "compliance_checklist": {{
    "broken_access_control": "PASS|FAIL|PARTIAL",
    "cryptographic_failures": "PASS|FAIL|PARTIAL",
    "injection": "PASS|FAIL|PARTIAL",
    "insecure_design": "PASS|FAIL|PARTIAL",
    "security_misconfiguration": "PASS|FAIL|PARTIAL",
    "vulnerable_components": "PASS|FAIL|PARTIAL",
    "authentication_failures": "PASS|FAIL|PARTIAL",
    "data_integrity_failures": "PASS|FAIL|PARTIAL",
    "logging_failures": "PASS|FAIL|PARTIAL",
    "ssrf": "PASS|FAIL|PARTIAL"
  }},
  "best_practices": {{
    "followed": ["string"],
    "missing": ["string"]
  }}
}}

SEVERITY GUIDELINES:
- CRITICAL: Immediate security risk, must fix before deployment
- HIGH: Significant risk, should fix soon
- MEDIUM: Moderate risk, fix when possible
- LOW: Minor issue, nice to fix

SECURITY RATING:
- 90-100: Excellent security posture
- 75-89: Good security with minor issues
- 60-74: Acceptable with some concerns
- 40-59: Poor security, needs improvement
- 0-39: Critical security issues

IMPORTANT:
- Be thorough but practical for MVP stage
- Focus on critical and high severity issues
- Provide actionable remediation steps
- Consider the hackathon/MVP context
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
        "vulnerabilities": raw_result.get("vulnerabilities", []),
        "severity_summary": raw_result.get("severity_summary", {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }),
        "remediation_suggestions": raw_result.get("remediation_suggestions", []),
        "security_rating": raw_result.get("security_rating", 0),
        "rating_justification": raw_result.get("rating_justification", ""),
        "compliance_checklist": raw_result.get("compliance_checklist", {}),
        "best_practices": raw_result.get("best_practices", {
            "followed": [],
            "missing": []
        }),
        "error": False
    }
    
    # Validate security rating is in range
    if not isinstance(structured["security_rating"], (int, float)):
        structured["security_rating"] = 50  # Default to neutral
    else:
        structured["security_rating"] = max(0, min(100, int(structured["security_rating"])))
    
    # Ensure lists are actually lists
    if not isinstance(structured["vulnerabilities"], list):
        structured["vulnerabilities"] = []
    
    if not isinstance(structured["remediation_suggestions"], list):
        structured["remediation_suggestions"] = []
    
    # Ensure dicts are actually dicts
    if not isinstance(structured["severity_summary"], dict):
        structured["severity_summary"] = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    
    if not isinstance(structured["compliance_checklist"], dict):
        structured["compliance_checklist"] = {}
    
    if not isinstance(structured["best_practices"], dict):
        structured["best_practices"] = {"followed": [], "missing": []}
    
    # Calculate severity summary if not provided
    if all(v == 0 for v in structured["severity_summary"].values()):
        for vuln in structured["vulnerabilities"]:
            severity = vuln.get("severity", "").lower()
            if severity in structured["severity_summary"]:
                structured["severity_summary"][severity] += 1
    
    return structured


def has_critical_issues(result: Dict[str, Any]) -> bool:
    """
    Check if there are any critical security issues.
    
    Args:
        result (Dict): Output from security_agent()
        
    Returns:
        bool: True if critical issues found
    """
    if result.get("error"):
        return False
    
    severity_summary = result.get("severity_summary", {})
    return severity_summary.get("critical", 0) > 0


def get_security_summary(result: Dict[str, Any]) -> str:
    """
    Generate a human-readable security summary.
    
    Args:
        result (Dict): Output from security_agent()
        
    Returns:
        str: Formatted summary
    """
    if result.get("error"):
        return f"Error: {result.get('message', 'Unknown error')}"
    
    rating = result.get("security_rating", 0)
    severity = result.get("severity_summary", {})
    
    # Determine rating level
    if rating >= 90:
        rating_level = "EXCELLENT ✅"
    elif rating >= 75:
        rating_level = "GOOD ✓"
    elif rating >= 60:
        rating_level = "ACCEPTABLE ⚠️"
    elif rating >= 40:
        rating_level = "POOR ⚠️"
    else:
        rating_level = "CRITICAL ❌"
    
    summary = f"""
SECURITY ANALYSIS SUMMARY
========================

Security Rating: {rating}/100 - {rating_level}
{result.get('rating_justification', '')}

VULNERABILITIES FOUND:
- Critical: {severity.get('critical', 0)}
- High: {severity.get('high', 0)}
- Medium: {severity.get('medium', 0)}
- Low: {severity.get('low', 0)}

Total Issues: {sum(severity.values())}
"""
    
    # Add critical issues warning
    if severity.get('critical', 0) > 0:
        summary += f"\n⚠️  WARNING: {severity['critical']} CRITICAL issues must be fixed before deployment!\n"
    
    # Add top remediation suggestions
    suggestions = result.get('remediation_suggestions', [])
    if suggestions:
        summary += "\nTOP REMEDIATION PRIORITIES:\n"
        for i, suggestion in enumerate(suggestions[:5], 1):
            summary += f"{i}. {suggestion}\n"
    
    return summary


def get_vulnerability_report(result: Dict[str, Any]) -> str:
    """
    Generate a detailed vulnerability report.
    
    Args:
        result (Dict): Output from security_agent()
        
    Returns:
        str: Formatted vulnerability report
    """
    if result.get("error"):
        return f"Error: {result.get('message', 'Unknown error')}"
    
    vulnerabilities = result.get("vulnerabilities", [])
    
    if not vulnerabilities:
        return "No vulnerabilities detected. Great job! ✅"
    
    report = "DETAILED VULNERABILITY REPORT\n"
    report += "=" * 50 + "\n\n"
    
    # Group by severity
    by_severity = {
        "CRITICAL": [],
        "HIGH": [],
        "MEDIUM": [],
        "LOW": []
    }
    
    for vuln in vulnerabilities:
        severity = vuln.get("severity", "LOW").upper()
        if severity in by_severity:
            by_severity[severity].append(vuln)
    
    # Report each severity level
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        vulns = by_severity[severity]
        if not vulns:
            continue
        
        report += f"\n{severity} SEVERITY ({len(vulns)} issues)\n"
        report += "-" * 50 + "\n"
        
        for i, vuln in enumerate(vulns, 1):
            report += f"\n{i}. {vuln.get('title', 'Unknown Issue')}\n"
            report += f"   Category: {vuln.get('category', 'N/A')}\n"
            report += f"   File: {vuln.get('file', 'N/A')}\n"
            if vuln.get('line'):
                report += f"   Line: {vuln.get('line')}\n"
            report += f"   Description: {vuln.get('description', 'N/A')}\n"
            report += f"   Remediation: {vuln.get('remediation', 'N/A')}\n"
            if vuln.get('cwe_id'):
                report += f"   CWE: {vuln.get('cwe_id')}\n"
    
    return report


def get_compliance_report(result: Dict[str, Any]) -> str:
    """
    Generate OWASP Top 10 compliance report.
    
    Args:
        result (Dict): Output from security_agent()
        
    Returns:
        str: Formatted compliance report
    """
    if result.get("error"):
        return f"Error: {result.get('message', 'Unknown error')}"
    
    checklist = result.get("compliance_checklist", {})
    
    report = """
OWASP TOP 10 COMPLIANCE REPORT
==============================

"""
    
    owasp_items = {
        "broken_access_control": "A01: Broken Access Control",
        "cryptographic_failures": "A02: Cryptographic Failures",
        "injection": "A03: Injection",
        "insecure_design": "A04: Insecure Design",
        "security_misconfiguration": "A05: Security Misconfiguration",
        "vulnerable_components": "A06: Vulnerable and Outdated Components",
        "authentication_failures": "A07: Identification and Authentication Failures",
        "data_integrity_failures": "A08: Software and Data Integrity Failures",
        "logging_failures": "A09: Security Logging and Monitoring Failures",
        "ssrf": "A10: Server-Side Request Forgery (SSRF)"
    }
    
    for key, name in owasp_items.items():
        status = checklist.get(key, "UNKNOWN")
        icon = "✅" if status == "PASS" else "⚠️" if status == "PARTIAL" else "❌"
        report += f"{icon} {name}: {status}\n"
    
    # Calculate pass rate
    total = len(owasp_items)
    passed = sum(1 for v in checklist.values() if v == "PASS")
    partial = sum(1 for v in checklist.values() if v == "PARTIAL")
    
    report += f"\nCompliance Score: {passed}/{total} passed, {partial}/{total} partial\n"
    
    return report


# Example usage and testing
if __name__ == "__main__":
    # Test with sample code scaffold
    test_scaffold = {
        "fastapi_scaffold": {
            "main.py": """
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
""",
            "models.py": """
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
"""
        },
        "react_scaffold": {
            "App.jsx": """
import React from 'react';

function App() {
    return <div>Hello World</div>;
}
"""
        }
    }
    
    print("Analyzing code security...")
    print("=" * 50)
    
    result = security_agent(test_scaffold)
    
    if result.get("error"):
        print(f"Error: {result.get('message')}")
    else:
        print(get_security_summary(result))
        print("\n" + "=" * 50)
        print(get_vulnerability_report(result))
        print("\n" + "=" * 50)
        print(get_compliance_report(result))
        
        # Check for critical issues
        if has_critical_issues(result):
            print("\n⚠️  CRITICAL ISSUES DETECTED - DO NOT DEPLOY!")
        else:
            print("\n✅ No critical issues - Safe to proceed")
        
        # Print full JSON for debugging
        print("\n" + "=" * 50)
        print("FULL JSON OUTPUT:")
        print(json.dumps(result, indent=2))

# Made with Bob
