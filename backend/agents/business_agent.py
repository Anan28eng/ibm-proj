"""
Business Insights Agent
Analyzes startup ideas and generates business strategy insights.

This agent provides:
- Target audience analysis
- Monetization strategies
- Competitor analysis
- Startup viability scoring
"""

import os
import json
from typing import Dict, List, Any, Optional
import google.generativeai as genai


def business_agent(idea: str) -> Dict[str, Any]:
    """
    Analyze a startup idea and generate comprehensive business insights.
    
    Args:
        idea (str): The startup idea description
        
    Returns:
        Dict containing:
            - target_audience: List of customer segments
            - monetization_strategy: Revenue model recommendations
            - competitor_analysis: List of competitors with analysis
            - viability_score: Score from 0-100
            - key_insights: Additional business insights
            
    Example:
        >>> result = business_agent("A mobile app for tracking daily water intake")
        >>> print(result['viability_score'])
        75
    """
    
    # Initialize Gemini client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Construct the prompt
    prompt = _build_prompt(idea)
    
    try:
        # Call Gemini API
        system_instruction = "You are an expert business strategist and startup advisor. Provide concise, actionable business insights in JSON format."
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1500
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
            "message": f"Business analysis failed: {str(e)}",
            "target_audience": [],
            "monetization_strategy": {},
            "competitor_analysis": [],
            "viability_score": 0,
            "key_insights": []
        }


def _build_prompt(idea: str) -> str:
    """
    Build the prompt for business analysis.
    
    Args:
        idea (str): The startup idea
        
    Returns:
        str: Formatted prompt
    """
    prompt = f"""Analyze this startup idea and provide comprehensive business insights:

STARTUP IDEA:
{idea}

Provide a detailed business analysis with the following structure:

1. TARGET AUDIENCE (3-5 specific customer segments)
   - For each segment, include:
     * Segment name
     * Demographics (age, income, location)
     * Pain points they experience
     * Why they would use this product

2. MONETIZATION STRATEGY
   - Primary revenue model (subscription, freemium, marketplace, etc.)
   - Pricing strategy and rationale
   - Revenue potential (low/medium/high)
   - Alternative revenue streams

3. COMPETITOR ANALYSIS (3-5 competitors)
   - For each competitor:
     * Company name
     * What they offer
     * Their strengths
     * Their weaknesses
     * How this idea is different/better

4. VIABILITY SCORE (0-100)
   - Overall startup viability score
   - Justification for the score
   - Key success factors
   - Major risks

5. KEY INSIGHTS
   - Market opportunity size
   - Go-to-market strategy recommendations
   - Critical success factors
   - Potential challenges

OUTPUT FORMAT:
Return ONLY valid JSON matching this exact structure:
{{
  "target_audience": [
    {{
      "segment_name": "string",
      "demographics": "string",
      "pain_points": ["string"],
      "value_proposition": "string"
    }}
  ],
  "monetization_strategy": {{
    "primary_model": "string",
    "pricing_strategy": "string",
    "revenue_potential": "low|medium|high",
    "alternative_streams": ["string"]
  }},
  "competitor_analysis": [
    {{
      "name": "string",
      "description": "string",
      "strengths": ["string"],
      "weaknesses": ["string"],
      "differentiation": "string"
    }}
  ],
  "viability_score": 0-100,
  "viability_justification": "string",
  "key_insights": {{
    "market_opportunity": "string",
    "go_to_market": "string",
    "success_factors": ["string"],
    "risks": ["string"]
  }}
}}

IMPORTANT:
- Be specific and actionable
- Base analysis on real market data when possible
- Keep descriptions concise (2-3 sentences max)
- Focus on MVP-stage considerations
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
        "target_audience": raw_result.get("target_audience", []),
        "monetization_strategy": raw_result.get("monetization_strategy", {}),
        "competitor_analysis": raw_result.get("competitor_analysis", []),
        "viability_score": raw_result.get("viability_score", 0),
        "viability_justification": raw_result.get("viability_justification", ""),
        "key_insights": raw_result.get("key_insights", {}),
        "error": False
    }
    
    # Validate viability score is in range
    if not isinstance(structured["viability_score"], (int, float)):
        structured["viability_score"] = 50  # Default to neutral
    else:
        structured["viability_score"] = max(0, min(100, int(structured["viability_score"])))
    
    # Ensure lists are actually lists
    if not isinstance(structured["target_audience"], list):
        structured["target_audience"] = []
    
    if not isinstance(structured["competitor_analysis"], list):
        structured["competitor_analysis"] = []
    
    # Ensure monetization_strategy is a dict
    if not isinstance(structured["monetization_strategy"], dict):
        structured["monetization_strategy"] = {}
    
    # Ensure key_insights is a dict
    if not isinstance(structured["key_insights"], dict):
        structured["key_insights"] = {}
    
    return structured


def get_business_summary(result: Dict[str, Any]) -> str:
    """
    Generate a human-readable summary of business insights.
    
    Args:
        result (Dict): Output from business_agent()
        
    Returns:
        str: Formatted summary
    """
    if result.get("error"):
        return f"Error: {result.get('message', 'Unknown error')}"
    
    summary = f"""
BUSINESS ANALYSIS SUMMARY
========================

Viability Score: {result['viability_score']}/100
{result.get('viability_justification', '')}

TARGET AUDIENCE:
"""
    
    for i, segment in enumerate(result.get('target_audience', []), 1):
        summary += f"\n{i}. {segment.get('segment_name', 'Unknown')}"
        summary += f"\n   Demographics: {segment.get('demographics', 'N/A')}"
        summary += f"\n   Pain Points: {', '.join(segment.get('pain_points', []))}"
    
    summary += f"\n\nMONETIZATION STRATEGY:"
    strategy = result.get('monetization_strategy', {})
    summary += f"\n- Model: {strategy.get('primary_model', 'N/A')}"
    summary += f"\n- Pricing: {strategy.get('pricing_strategy', 'N/A')}"
    summary += f"\n- Revenue Potential: {strategy.get('revenue_potential', 'N/A')}"
    
    summary += f"\n\nCOMPETITORS:"
    for i, comp in enumerate(result.get('competitor_analysis', []), 1):
        summary += f"\n{i}. {comp.get('name', 'Unknown')}"
        summary += f"\n   Differentiation: {comp.get('differentiation', 'N/A')}"
    
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
    
    print("Analyzing startup idea...")
    print("=" * 50)
    
    result = business_agent(test_idea)
    
    if result.get("error"):
        print(f"Error: {result.get('message')}")
    else:
        print(f"\nViability Score: {result['viability_score']}/100")
        print(f"\nTarget Audience Segments: {len(result['target_audience'])}")
        print(f"Competitors Identified: {len(result['competitor_analysis'])}")
        print(f"\nPrimary Revenue Model: {result['monetization_strategy'].get('primary_model', 'N/A')}")
        
        print("\n" + "=" * 50)
        print(get_business_summary(result))
        
        # Print full JSON for debugging
        print("\n" + "=" * 50)
        print("FULL JSON OUTPUT:")
        print(json.dumps(result, indent=2))

# Made with Bob
