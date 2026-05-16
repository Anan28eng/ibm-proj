# AI Venture Studio - Detailed Agent Specifications

This document provides detailed specifications for each agent, including prompt templates, input/output schemas, and implementation guidelines.

---

## Agent 1: Idea Analyzer

### Purpose
Parse and validate startup ideas, extracting structured information for downstream agents.

### Input Schema
```python
class IdeaInput(BaseModel):
    raw_idea: str
    additional_context: Optional[str] = None
```

### Output Schema
```python
class IdeaAnalysis(BaseModel):
    is_valid: bool
    validation_errors: List[str] = []
    problem_statement: str
    proposed_solution: str
    target_market: str
    unique_value_proposition: str
    complexity_score: int  # 1-10
    key_features: List[str]
    success_metrics: List[str]
    estimated_timeline: str  # e.g., "3-6 months"
```

### Prompt Template
```
You are an expert startup analyst. Analyze the following startup idea and extract structured information.

STARTUP IDEA:
{raw_idea}

TASK:
Extract and validate the following components:
1. Problem Statement: What problem does this solve?
2. Proposed Solution: How does it solve the problem?
3. Target Market: Who are the primary users/customers?
4. Unique Value Proposition: What makes this different?
5. Complexity Score: Rate implementation complexity (1=simple, 10=very complex)
6. Key Features: List 3-5 core features
7. Success Metrics: How to measure success?
8. Estimated Timeline: Realistic MVP development time

VALIDATION RULES:
- Idea must have a clear problem and solution
- Target market must be specific
- Must be technically feasible

OUTPUT FORMAT:
Return a JSON object matching this schema:
{
  "is_valid": boolean,
  "validation_errors": [list of issues if invalid],
  "problem_statement": "string",
  "proposed_solution": "string",
  "target_market": "string",
  "unique_value_proposition": "string",
  "complexity_score": number,
  "key_features": ["feature1", "feature2", ...],
  "success_metrics": ["metric1", "metric2", ...],
  "estimated_timeline": "string"
}
```

### Token Budget: 500-1000 tokens

### Implementation Notes
- Use JSON mode for structured output
- Implement strict validation on output
- Return early if idea is invalid
- Log validation errors for user feedback

---

## Agent 2: Business Insights

### Purpose
Generate comprehensive business strategy and market analysis.

### Input Schema
```python
class BusinessInsightsInput(BaseModel):
    idea_analysis: IdeaAnalysis
```

### Output Schema
```python
class Competitor(BaseModel):
    name: str
    description: str
    strengths: List[str]
    weaknesses: List[str]

class RevenueModel(BaseModel):
    type: str  # e.g., "subscription", "freemium", "marketplace"
    description: str
    pricing_strategy: str

class BusinessInsights(BaseModel):
    customer_segments: List[str]
    competitors: List[Competitor]  # Max 5
    revenue_models: List[RevenueModel]
    go_to_market_strategy: str
    key_risks: List[str]
    mitigation_strategies: List[str]
    market_size_estimate: str
    competitive_advantages: List[str]
```

### Prompt Template
```
You are a business strategy consultant. Generate comprehensive business insights for this startup.

STARTUP CONTEXT:
Problem: {problem_statement}
Solution: {proposed_solution}
Target Market: {target_market}
UVP: {unique_value_proposition}

TASK:
Provide detailed business analysis covering:

1. CUSTOMER SEGMENTS (3-5 specific segments)
   - Demographics, psychographics, pain points

2. COMPETITIVE ANALYSIS (3-5 competitors)
   - Direct and indirect competitors
   - Their strengths and weaknesses
   - Market positioning

3. REVENUE MODELS (2-3 options)
   - Model type and description
   - Pricing strategy
   - Scalability potential

4. GO-TO-MARKET STRATEGY
   - Customer acquisition channels
   - Marketing approach
   - Launch timeline

5. RISK ANALYSIS
   - Key risks (market, technical, financial)
   - Mitigation strategies

6. MARKET OPPORTUNITY
   - Market size estimate
   - Growth potential
   - Competitive advantages

OUTPUT FORMAT:
Return JSON matching the BusinessInsights schema.
Keep descriptions concise (2-3 sentences max).
Focus on actionable insights.
```

### Token Budget: 1500-2000 tokens

### Implementation Notes
- Limit competitor analysis to top 5
- Use bullet points for conciseness
- Prioritize actionable insights over theory
- Include market size estimates with sources

---

## Agent 3: Technical Architecture

### Purpose
Design system architecture and recommend technology stack.

### Input Schema
```python
class TechArchitectureInput(BaseModel):
    idea_analysis: IdeaAnalysis
    business_insights: BusinessInsights
```

### Output Schema
```python
class TechStack(BaseModel):
    frontend: List[str]
    backend: List[str]
    database: List[str]
    infrastructure: List[str]
    third_party_services: List[str]

class DataModel(BaseModel):
    entity_name: str
    attributes: List[str]
    relationships: List[str]

class APIEndpoint(BaseModel):
    method: str
    path: str
    description: str
    request_body: Optional[str]
    response: Optional[str]

class TechnicalArchitecture(BaseModel):
    architecture_pattern: str  # e.g., "monolith", "microservices"
    tech_stack: TechStack
    data_models: List[DataModel]
    api_endpoints: List[APIEndpoint]
    system_components: List[str]
    scalability_considerations: List[str]
    security_requirements: List[str]
    deployment_strategy: str
```

### Prompt Template
```
You are a senior software architect. Design a technical architecture for this startup MVP.

PROJECT CONTEXT:
Problem: {problem_statement}
Solution: {proposed_solution}
Key Features: {key_features}
Complexity: {complexity_score}/10
Timeline: {estimated_timeline}

REQUIREMENTS:
- MVP-focused (not over-engineered)
- Modern, maintainable tech stack
- Scalable architecture
- Security best practices
- Cost-effective for early stage

TASK:
Design comprehensive technical architecture including:

1. ARCHITECTURE PATTERN
   - Monolith vs microservices
   - Justification for choice

2. TECH STACK
   - Frontend framework and libraries
   - Backend framework and language
   - Database (SQL/NoSQL)
   - Infrastructure (cloud provider, containers)
   - Third-party services (auth, payments, etc.)

3. DATA MODELS (5-10 core entities)
   - Entity name
   - Key attributes
   - Relationships

4. API DESIGN (10-15 endpoints)
   - HTTP method and path
   - Purpose
   - Request/response structure

5. SYSTEM COMPONENTS
   - Major components and their responsibilities
   - Communication patterns

6. SCALABILITY
   - How to scale each component
   - Performance considerations

7. SECURITY
   - Authentication/authorization
   - Data protection
   - API security

8. DEPLOYMENT
   - Deployment strategy
   - CI/CD pipeline
   - Monitoring and logging

OUTPUT FORMAT:
Return JSON matching TechnicalArchitecture schema.
Be specific with technology choices.
Justify major decisions.
```

### Token Budget: 2000-3000 tokens

### Implementation Notes
- Prefer proven technologies over bleeding edge
- Consider team expertise when recommending stack
- Balance simplicity with scalability
- Include deployment considerations early

---

## Agent 4: Code Scaffolding

### Purpose
Generate complete MVP code scaffold with all necessary files.

### Input Schema
```python
class CodeScaffoldInput(BaseModel):
    technical_architecture: TechnicalArchitecture
    idea_analysis: IdeaAnalysis
```

### Output Schema
```python
class CodeFile(BaseModel):
    path: str
    content: str
    language: str
    description: str

class CodeScaffold(BaseModel):
    project_name: str
    files: List[CodeFile]
    setup_instructions: str
    dependencies: Dict[str, List[str]]  # {"backend": [...], "frontend": [...]}
    environment_variables: List[str]
    folder_structure: str  # ASCII tree
```

### Prompt Template
```
You are an expert full-stack developer. Generate a complete MVP code scaffold.

PROJECT SPECIFICATIONS:
Architecture: {architecture_pattern}
Tech Stack:
- Frontend: {frontend_stack}
- Backend: {backend_stack}
- Database: {database}

Data Models: {data_models}
API Endpoints: {api_endpoints}

TASK:
Generate a complete, runnable code scaffold including:

1. PROJECT STRUCTURE
   - Organized folder hierarchy
   - Separation of concerns
   - Best practices for chosen stack

2. BACKEND CODE
   - API endpoints implementation
   - Database models
   - Authentication/authorization
   - Error handling
   - Configuration management

3. FRONTEND CODE
   - Component structure
   - API client
   - State management
   - Routing
   - Basic styling

4. CONFIGURATION FILES
   - Package managers (package.json, requirements.txt)
   - Environment configuration
   - Docker files
   - CI/CD configuration

5. DOCUMENTATION
   - README with setup instructions
   - API documentation
   - Environment variables guide

REQUIREMENTS:
- Code must be production-ready
- Include error handling
- Add comments for complex logic
- Follow language-specific conventions
- Include basic tests

OUTPUT FORMAT:
Return JSON with array of files:
{
  "project_name": "string",
  "files": [
    {
      "path": "relative/path/to/file.ext",
      "content": "complete file content",
      "language": "python|javascript|typescript|etc",
      "description": "brief description"
    }
  ],
  "setup_instructions": "step-by-step setup guide",
  "dependencies": {
    "backend": ["package1", "package2"],
    "frontend": ["package1", "package2"]
  },
  "environment_variables": ["VAR1", "VAR2"],
  "folder_structure": "ASCII tree representation"
}

IMPORTANT:
- Generate COMPLETE files, not snippets
- Include all necessary imports
- Add proper error handling
- Follow security best practices
```

### Token Budget: 4000-6000 tokens (largest agent)

### Implementation Notes
- Generate files in logical order (config → models → routes → components)
- Use templates for common patterns
- Validate generated code syntax if possible
- Split into multiple LLM calls if needed
- Consider using code generation libraries

### Code Generation Strategy
```python
# Pseudo-code for code generation
async def generate_scaffold(self, input_data):
    # Step 1: Generate project structure
    structure = await self._generate_structure()
    
    # Step 2: Generate backend files
    backend_files = await self._generate_backend(
        models=input_data.data_models,
        endpoints=input_data.api_endpoints
    )
    
    # Step 3: Generate frontend files
    frontend_files = await self._generate_frontend(
        components=self._extract_components(input_data)
    )
    
    # Step 4: Generate config files
    config_files = await self._generate_configs(
        tech_stack=input_data.tech_stack
    )
    
    # Step 5: Combine and validate
    all_files = backend_files + frontend_files + config_files
    return CodeScaffold(files=all_files, ...)
```

---

## Agent 5: Security Review

### Purpose
Identify security vulnerabilities and recommend fixes.

### Input Schema
```python
class SecurityReviewInput(BaseModel):
    code_scaffold: CodeScaffold
    technical_architecture: TechnicalArchitecture
```

### Output Schema
```python
class SecurityIssue(BaseModel):
    severity: str  # "critical", "high", "medium", "low"
    category: str  # "authentication", "injection", "xss", etc.
    file_path: str
    line_number: Optional[int]
    description: str
    recommendation: str
    cwe_id: Optional[str]  # Common Weakness Enumeration ID

class SecurityReport(BaseModel):
    overall_score: int  # 0-100
    has_critical_issues: bool
    issues: List[SecurityIssue]
    security_checklist: Dict[str, bool]
    recommendations: List[str]
    compliant_standards: List[str]  # e.g., ["OWASP Top 10"]
```

### Prompt Template
```
You are a security expert conducting a code security review.

CODE TO REVIEW:
{code_files_summary}

ARCHITECTURE:
{architecture_summary}

TASK:
Perform comprehensive security analysis covering:

1. AUTHENTICATION & AUTHORIZATION
   - Proper authentication implementation
   - Authorization checks
   - Session management
   - Password handling

2. INPUT VALIDATION
   - SQL injection prevention
   - XSS prevention
   - CSRF protection
   - Input sanitization

3. DATA PROTECTION
   - Sensitive data encryption
   - Secure data storage
   - API key management
   - Environment variable usage

4. API SECURITY
   - Rate limiting
   - CORS configuration
   - API authentication
   - Error message exposure

5. DEPENDENCY SECURITY
   - Known vulnerable packages
   - Outdated dependencies
   - Supply chain risks

6. CONFIGURATION
   - Debug mode disabled
   - Secure defaults
   - HTTPS enforcement
   - Security headers

SEVERITY LEVELS:
- CRITICAL: Immediate security risk, must fix before deployment
- HIGH: Significant risk, should fix soon
- MEDIUM: Moderate risk, fix when possible
- LOW: Minor issue, nice to fix

OUTPUT FORMAT:
Return JSON matching SecurityReport schema.
For each issue, provide:
- Clear description
- Specific file and line number
- Actionable recommendation
- CWE ID if applicable

SECURITY CHECKLIST:
Evaluate against OWASP Top 10:
- Broken Access Control
- Cryptographic Failures
- Injection
- Insecure Design
- Security Misconfiguration
- Vulnerable Components
- Authentication Failures
- Data Integrity Failures
- Logging Failures
- SSRF
```

### Token Budget: 1000-1500 tokens

### Implementation Notes
- Use static analysis tools if available
- Check against OWASP Top 10
- Prioritize critical issues
- Provide specific fix recommendations
- Include code examples for fixes

### Security Checklist
```python
SECURITY_CHECKLIST = {
    "authentication": [
        "Password hashing implemented",
        "Session management secure",
        "Multi-factor auth supported"
    ],
    "authorization": [
        "Role-based access control",
        "Resource-level permissions",
        "API endpoint protection"
    ],
    "input_validation": [
        "SQL injection prevention",
        "XSS prevention",
        "CSRF tokens implemented"
    ],
    "data_protection": [
        "Sensitive data encrypted",
        "Secure key storage",
        "HTTPS enforced"
    ],
    "api_security": [
        "Rate limiting enabled",
        "CORS properly configured",
        "API versioning"
    ]
}
```

---

## Agent 6: GitHub PR Workflow

### Purpose
Prepare code for GitHub integration with comprehensive documentation.

### Input Schema
```python
class GitHubWorkflowInput(BaseModel):
    idea_analysis: IdeaAnalysis
    business_insights: BusinessInsights
    technical_architecture: TechnicalArchitecture
    code_scaffold: CodeScaffold
    security_report: SecurityReport
```

### Output Schema
```python
class GitHubPackage(BaseModel):
    pr_title: str
    pr_description: str
    commit_messages: List[str]
    changelog: str
    github_actions_workflow: str
    issue_templates: List[Dict[str, str]]
    contributing_guide: str
    code_of_conduct: str
    readme_additions: str
```

### Prompt Template
```
You are a DevOps engineer preparing code for GitHub integration.

PROJECT CONTEXT:
Name: {project_name}
Description: {problem_statement}
Tech Stack: {tech_stack}
Security Score: {security_score}/100

TASK:
Generate comprehensive GitHub integration package:

1. PULL REQUEST
   - Compelling PR title
   - Detailed PR description with:
     * What was built
     * Key features
     * Technical decisions
     * Testing performed
     * Security considerations

2. COMMIT MESSAGES (5-10 logical commits)
   - Follow conventional commits format
   - Group related changes
   - Clear, descriptive messages

3. CHANGELOG
   - Version 0.1.0 (Initial MVP)
   - All features implemented
   - Known limitations

4. GITHUB ACTIONS WORKFLOW
   - CI/CD pipeline
   - Automated testing
   - Linting and formatting
   - Security scanning
   - Deployment (optional)

5. ISSUE TEMPLATES
   - Bug report template
   - Feature request template
   - Question template

6. CONTRIBUTING GUIDE
   - How to contribute
   - Code style guidelines
   - PR process
   - Development setup

7. CODE OF CONDUCT
   - Community guidelines
   - Expected behavior
   - Enforcement

8. README ADDITIONS
   - Badges (build status, coverage)
   - Quick start guide
   - API documentation link
   - License information

OUTPUT FORMAT:
Return JSON matching GitHubPackage schema.
Use markdown formatting for documentation.
Follow GitHub best practices.
```

### Token Budget: 800-1200 tokens

### Implementation Notes
- Use conventional commit format
- Include CI/CD best practices
- Add security scanning to workflow
- Generate comprehensive documentation
- Include badges and shields

### GitHub Actions Template
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          # Backend tests
          cd backend && pytest
          # Frontend tests
          cd frontend && npm test

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Security scan
        run: |
          # Dependency check
          # SAST scanning

  deploy:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: echo "Deploy steps here"
```

---

## Cross-Agent Communication

### Data Flow Between Agents
```python
# Agent 1 → Agent 2
idea_analysis = await agent1.execute(raw_idea)

# Agent 2 → Agent 3
business_insights = await agent2.execute(idea_analysis)

# Agent 3 → Agent 4
tech_architecture = await agent3.execute({
    "idea_analysis": idea_analysis,
    "business_insights": business_insights
})

# Agent 4 → Agent 5
code_scaffold = await agent4.execute(tech_architecture)

# Agent 5 → Agent 6
security_report = await agent5.execute(code_scaffold)

# Agent 6 (final)
github_package = await agent6.execute({
    "idea_analysis": idea_analysis,
    "business_insights": business_insights,
    "tech_architecture": tech_architecture,
    "code_scaffold": code_scaffold,
    "security_report": security_report
})
```

### Error Handling Pattern
```python
class AgentExecutionError(Exception):
    def __init__(self, agent_name: str, stage: str, message: str):
        self.agent_name = agent_name
        self.stage = stage
        self.message = message

async def execute_with_retry(agent, input_data, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await agent.execute(input_data)
        except Exception as e:
            if attempt == max_retries - 1:
                raise AgentExecutionError(
                    agent_name=agent.name,
                    stage=agent.current_stage,
                    message=str(e)
                )
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

---

## Testing Strategy

### Unit Tests for Each Agent
```python
@pytest.mark.asyncio
async def test_idea_analyzer_valid_idea():
    agent = IdeaAnalyzer(llm_client, config)
    result = await agent.execute({
        "raw_idea": "A mobile app for tracking water intake"
    })
    assert result["is_valid"] == True
    assert "problem_statement" in result

@pytest.mark.asyncio
async def test_idea_analyzer_invalid_idea():
    agent = IdeaAnalyzer(llm_client, config)
    result = await agent.execute({
        "raw_idea": "An app"  # Too vague
    })
    assert result["is_valid"] == False
    assert len(result["validation_errors"]) > 0
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_full_pipeline():
    orchestrator = Pipeline(agents, config)
    result = await orchestrator.execute(sample_idea)
    
    assert "idea_analysis" in result
    assert "business_insights" in result
    assert "technical_architecture" in result
    assert "code_scaffold" in result
    assert "security_report" in result
    assert "github_package" in result
```

---

## Performance Optimization

### Token Usage Tracking
```python
class TokenTracker:
    def __init__(self):
        self.usage = {}
    
    def track(self, agent_name: str, tokens: int):
        if agent_name not in self.usage:
            self.usage[agent_name] = []
        self.usage[agent_name].append(tokens)
    
    def get_total(self) -> int:
        return sum(sum(tokens) for tokens in self.usage.values())
    
    def get_average(self, agent_name: str) -> float:
        if agent_name not in self.usage:
            return 0
        return sum(self.usage[agent_name]) / len(self.usage[agent_name])
```

### Caching Strategy
```python
from functools import lru_cache
import hashlib

def cache_key(input_data: dict) -> str:
    """Generate cache key from input data"""
    return hashlib.md5(
        json.dumps(input_data, sort_keys=True).encode()
    ).hexdigest()

@lru_cache(maxsize=100)
async def cached_execute(agent, cache_key: str, input_data: dict):
    """Cache agent execution results"""
    return await agent.execute(input_data)
```

---

## Monitoring & Observability

### Logging Structure
```python
import structlog

logger = structlog.get_logger()

# Log agent execution
logger.info(
    "agent_execution_started",
    agent=agent.name,
    input_size=len(str(input_data)),
    timestamp=datetime.utcnow()
)

# Log completion
logger.info(
    "agent_execution_completed",
    agent=agent.name,
    tokens_used=tokens,
    duration_seconds=duration,
    success=True
)
```

### Metrics to Track
- Agent execution time
- Token usage per agent
- Success/failure rate
- Error types and frequency
- End-to-end pipeline latency
- User satisfaction scores

---

This specification provides everything needed to implement each agent with consistency and quality. Use these templates as starting points and adjust based on actual LLM performance and user feedback.