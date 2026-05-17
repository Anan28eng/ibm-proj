"""
AI Venture Studio Orchestrator
Coordinates the sequential execution of all agents to generate a complete MVP.

Pipeline Flow:
1. Business Agent - Analyze business viability
2. Architect Agent - Design technical architecture
3. Builder Agent - Generate code scaffold
4. Security Agent - Review security
5. GitHub Agent - Prepare GitHub integration

Each agent's output feeds into the next, creating a comprehensive MVP package.
"""

import time
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime

# Import all agents
from agents.business_agent import business_agent
from agents.architect_agent import architect_agent
from agents.builder_agent import builder_agent
from agents.security_agent import security_agent, has_critical_issues
from agents.github_agent import github_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PipelineStatus:
    """Track pipeline execution status."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class VentureStudioOrchestrator:
    """
    Orchestrates the sequential execution of all agents.
    
    Attributes:
        idea (str): The startup idea to process
        status (Dict): Current status of each agent
        outputs (Dict): Collected outputs from each agent
        errors (Dict): Any errors encountered
        start_time (float): Pipeline start timestamp
        end_time (float): Pipeline end timestamp
    """
    
    def __init__(self, idea: str, options: Optional[Dict[str, Any]] = None):
        """
        Initialize the orchestrator.
        
        Args:
            idea (str): The startup idea description
            options (Dict, optional): Configuration options
        """
        self.idea = idea
        self.options = options or {}
        
        # Pipeline state
        self.status = {
            "business": PipelineStatus.PENDING,
            "architect": PipelineStatus.PENDING,
            "builder": PipelineStatus.PENDING,
            "security": PipelineStatus.PENDING,
            "github": PipelineStatus.PENDING
        }
        
        self.outputs = {}
        self.errors = {}
        self.start_time = None
        self.end_time = None
        
        # Configuration
        self.stop_on_critical_security = self.options.get("stop_on_critical_security", True)
        self.skip_github = self.options.get("skip_github", False)
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the complete pipeline sequentially.
        
        Returns:
            Dict containing all outputs, status, and metadata
        """
        self.start_time = time.time()
        
        try:
            # Step 1: Business Analysis
            self._execute_agent(
                name="business",
                agent_func=business_agent,
                args=(self.idea,),
                description="Analyzing business viability"
            )
            
            # Step 2: Technical Architecture
            self._execute_agent(
                name="architect",
                agent_func=architect_agent,
                args=(self.idea, self.outputs.get("business")),
                description="Designing technical architecture"
            )
            
            # Step 3: Code Generation
            self._execute_agent(
                name="builder",
                agent_func=builder_agent,
                args=(self.idea, self.outputs.get("architect")),
                description="Generating code scaffold"
            )
            
            # Step 4: Security Review
            self._execute_agent(
                name="security",
                agent_func=security_agent,
                args=(self.outputs.get("builder"), self.outputs.get("architect")),
                description="Reviewing security"
            )
            
            # Check for critical security issues
            if self.stop_on_critical_security and self.outputs.get("security"):
                if has_critical_issues(self.outputs["security"]):
                    self.errors["security"] = "Critical security issues detected"
                    self.status["github"] = PipelineStatus.SKIPPED
                    return self._build_response(success=False)
            
            # Step 5: GitHub Integration (optional)
            if not self.skip_github:
                self._execute_agent(
                    name="github",
                    agent_func=github_agent,
                    args=(
                        self.idea,
                        self.outputs.get("builder"),
                        self.outputs.get("security"),
                        self.outputs.get("architect")
                    ),
                    description="Preparing GitHub integration"
                )
            else:
                self.status["github"] = PipelineStatus.SKIPPED
            
            self.end_time = time.time()
            return self._build_response(success=True)
            
        except Exception as e:
            self.end_time = time.time()
            self.errors["pipeline"] = str(e)
            return self._build_response(success=False)
    
    def _execute_agent(
        self,
        name: str,
        agent_func: Callable,
        args: tuple,
        description: str
    ) -> None:
        """
        Execute a single agent and track its status.
        
        Args:
            name (str): Agent name
            agent_func (Callable): Agent function to execute
            args (tuple): Arguments to pass to agent
            description (str): Human-readable description
        """
        print(f"[{name.upper()}] {description}...")
        self.status[name] = PipelineStatus.IN_PROGRESS
        
        try:
            start = time.time()
            result = agent_func(*args)
            duration = time.time() - start
            
            # Check for errors in result
            if result.get("error"):
                self.status[name] = PipelineStatus.FAILED
                self.errors[name] = result.get("message", "Unknown error")
                print(f"[{name.upper()}] ❌ Failed: {self.errors[name]}")
                raise Exception(f"{name} agent failed: {self.errors[name]}")
            
            self.outputs[name] = result
            self.status[name] = PipelineStatus.COMPLETED
            print(f"[{name.upper()}] ✓ Completed in {duration:.2f}s")
            
        except Exception as e:
            self.status[name] = PipelineStatus.FAILED
            self.errors[name] = str(e)
            print(f"[{name.upper()}] ❌ Error: {str(e)}")
            raise
    
    def _build_response(self, success: bool) -> Dict[str, Any]:
        """
        Build the final pipeline response.
        
        Args:
            success (bool): Whether pipeline completed successfully
            
        Returns:
            Dict: Complete pipeline response
        """
        duration = (self.end_time - self.start_time) if self.end_time else 0
        
        return {
            "success": success,
            "idea": self.idea,
            "status": self.status,
            "outputs": self.outputs,
            "errors": self.errors,
            "metadata": {
                "start_time": datetime.fromtimestamp(self.start_time).isoformat() if self.start_time else None,
                "end_time": datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
                "duration_seconds": round(duration, 2),
                "agents_completed": sum(1 for s in self.status.values() if s == PipelineStatus.COMPLETED),
                "agents_failed": sum(1 for s in self.status.values() if s == PipelineStatus.FAILED),
                "agents_skipped": sum(1 for s in self.status.values() if s == PipelineStatus.SKIPPED)
            }
        }
    
    def get_status(self) -> Dict[str, str]:
        """Get current status of all agents."""
        return self.status.copy()
    
    def get_progress_percentage(self) -> int:
        """Calculate overall progress percentage."""
        total_agents = len(self.status)
        completed = sum(1 for s in self.status.values() if s in [PipelineStatus.COMPLETED, PipelineStatus.SKIPPED])
        return int((completed / total_agents) * 100)


def generate_mvp(idea: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Main entry point to generate a complete MVP from an idea.
    
    This is the primary function to use for generating MVPs. It orchestrates
    all agents sequentially and returns a comprehensive result.
    
    Args:
        idea (str): The startup idea description
        options (Dict, optional): Configuration options:
            - stop_on_critical_security (bool): Stop if critical security issues found (default: True)
            - skip_github (bool): Skip GitHub integration (default: False)
    
    Returns:
        Dict containing:
            - success (bool): Whether pipeline completed successfully
            - idea (str): The original idea
            - status (Dict): Status of each agent
            - outputs (Dict): All agent outputs
            - errors (Dict): Any errors encountered
            - metadata (Dict): Execution metadata
    
    Example:
        >>> result = generate_mvp("A mobile app for tracking water intake")
        >>> if result['success']:
        >>>     print(f"MVP generated in {result['metadata']['duration_seconds']}s")
        >>>     print(f"Security rating: {result['outputs']['security']['security_rating']}/100")
    """
    orchestrator = VentureStudioOrchestrator(idea, options)
    return orchestrator.execute()


def get_pipeline_summary(result: Dict[str, Any]) -> str:
    """
    Generate a human-readable summary of the pipeline execution.
    
    Args:
        result (Dict): Output from generate_mvp()
        
    Returns:
        str: Formatted summary
    """
    if not result:
        return "No pipeline result available"
    
    metadata = result.get("metadata", {})
    outputs = result.get("outputs", {})
    errors = result.get("errors", {})
    
    summary = f"""
AI VENTURE STUDIO - PIPELINE SUMMARY
====================================

Status: {'✅ SUCCESS' if result.get('success') else '❌ FAILED'}
Duration: {metadata.get('duration_seconds', 0)}s
Agents Completed: {metadata.get('agents_completed', 0)}/5

IDEA:
{result.get('idea', 'N/A')[:200]}...

RESULTS:
"""
    
    # Business Analysis
    if "business" in outputs:
        business = outputs["business"]
        summary += f"\n✓ Business Analysis:"
        summary += f"\n  - Viability Score: {business.get('viability_score', 0)}/100"
        summary += f"\n  - Target Segments: {len(business.get('target_audience', []))}"
        summary += f"\n  - Competitors: {len(business.get('competitor_analysis', []))}"
    elif "business" in errors:
        summary += f"\n✗ Business Analysis: {errors['business']}"
    
    # Architecture
    if "architect" in outputs:
        arch = outputs["architect"]
        frontend = arch.get('frontend_stack', {})
        backend = arch.get('backend_stack', {})
        summary += f"\n✓ Technical Architecture:"
        summary += f"\n  - Frontend: {frontend.get('framework', 'N/A')}"
        summary += f"\n  - Backend: {backend.get('framework', 'N/A')}"
        summary += f"\n  - Database: {arch.get('database_schema', {}).get('database_type', 'N/A')}"
    elif "architect" in errors:
        summary += f"\n✗ Technical Architecture: {errors['architect']}"
    
    # Code Generation
    if "builder" in outputs:
        builder = outputs["builder"]
        react_files = len(builder.get('react_scaffold', {}))
        fastapi_files = len(builder.get('fastapi_scaffold', {}))
        summary += f"\n✓ Code Generation:"
        summary += f"\n  - React Files: {react_files}"
        summary += f"\n  - FastAPI Files: {fastapi_files}"
        summary += f"\n  - Total Files: {react_files + fastapi_files}"
    elif "builder" in errors:
        summary += f"\n✗ Code Generation: {errors['builder']}"
    
    # Security Review
    if "security" in outputs:
        security = outputs["security"]
        severity = security.get('severity_summary', {})
        summary += f"\n✓ Security Review:"
        summary += f"\n  - Security Rating: {security.get('security_rating', 0)}/100"
        summary += f"\n  - Critical Issues: {severity.get('critical', 0)}"
        summary += f"\n  - Total Issues: {sum(severity.values())}"
    elif "security" in errors:
        summary += f"\n✗ Security Review: {errors['security']}"
    
    # GitHub Integration
    if "github" in outputs:
        github = outputs["github"]
        repo = github.get('repository_status', {})
        summary += f"\n✓ GitHub Integration:"
        summary += f"\n  - Repository: {repo.get('name', 'N/A')}"
        summary += f"\n  - Commits: {len(github.get('commit_summary', []))}"
        summary += f"\n  - Docs Generated: {len(github.get('documentation', {}))}"
    elif "github" in errors:
        summary += f"\n✗ GitHub Integration: {errors['github']}"
    
    return summary


def validate_idea(idea: str) -> Dict[str, Any]:
    """
    Quick validation of idea before running full pipeline.
    
    Args:
        idea (str): The startup idea
        
    Returns:
        Dict with validation result
    """
    if not idea or not isinstance(idea, str):
        return {
            "valid": False,
            "error": "Idea must be a non-empty string"
        }
    
    if len(idea.strip()) < 20:
        return {
            "valid": False,
            "error": "Idea is too short. Please provide more details (at least 20 characters)"
        }
    
    if len(idea) > 5000:
        return {
            "valid": False,
            "error": "Idea is too long. Please keep it under 5000 characters"
        }
    
    return {
        "valid": True,
        "idea_length": len(idea),
        "word_count": len(idea.split())
    }


async def run_pipeline(idea: str, live_mode: bool = False) -> Dict[str, Any]:
    """
    Main pipeline function for sequential agent execution.
    
    This function orchestrates the execution of all agents in sequence:
    1. business_agent - Analyze business viability
    2. architect_agent - Design technical architecture
    3. builder_agent - Generate code scaffold
    4. security_agent - Review security
    5. github_agent - Prepare GitHub integration
    
    Args:
        idea (str): The startup idea description
        live_mode (bool): If False, returns mock data for testing (default: False)
    
    Returns:
        Dict containing:
            - success (bool): Whether pipeline completed successfully
            - idea (str): The original idea
            - live_mode (bool): Whether live mode was used
            - stages (Dict): Results from each agent stage
            - errors (List): Any errors encountered
            - metadata (Dict): Execution metadata
    
    Example:
        >>> result = await run_pipeline("A mobile app for tracking water intake", live_mode=True)
        >>> if result['success']:
        >>>     print(f"Pipeline completed in {result['metadata']['duration_seconds']}s")
    """
    start_time = time.time()
    
    # Initialize response structure
    response = {
        "success": False,
        "idea": idea,
        "live_mode": live_mode,
        "stages": {
            "business": None,
            "architect": None,
            "builder": None,
            "security": None,
            "github": None
        },
        "errors": [],
        "metadata": {
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "duration_seconds": 0,
            "stages_completed": 0,
            "stages_failed": 0
        }
    }
    
    # Mock mode - return test data without calling agents
    if not live_mode:
        logger.info("Running in MOCK mode - returning test data")
        response["success"] = True
        response["stages"] = {
            "business": {"viability_score": 85, "mock": True},
            "architect": {"architecture": "mock_architecture", "mock": True},
            "builder": {"scaffold": "mock_scaffold", "mock": True},
            "security": {"security_rating": 90, "mock": True},
            "github": {"repository": "mock_repo", "mock": True}
        }
        response["metadata"]["stages_completed"] = 5
        response["metadata"]["duration_seconds"] = 0.1
        response["metadata"]["end_time"] = datetime.now().isoformat()
        logger.info("Mock pipeline completed successfully")
        return response
    
    try:
        logger.info("=" * 80)
        logger.info("STARTING AI VENTURE STUDIO PIPELINE")
        logger.info(f"Idea: {idea[:100]}...")
        logger.info("=" * 80)
        
        # Stage 1: Business Agent
        logger.info("\n[STAGE 1/5] Starting Business Analysis...")
        try:
            stage_start = time.time()
            business_result = business_agent(idea)
            stage_duration = time.time() - stage_start
            
            if business_result.get("error"):
                raise Exception(business_result.get("message", "Business agent failed"))
            
            response["stages"]["business"] = business_result
            response["metadata"]["stages_completed"] += 1
            logger.info(f"✓ Business Analysis completed in {stage_duration:.2f}s")
            logger.info(f"  Viability Score: {business_result.get('viability_score', 'N/A')}/100")
            
        except Exception as e:
            error_msg = f"Business Agent failed: {str(e)}"
            logger.error(f"✗ {error_msg}")
            response["errors"].append({"stage": "business", "error": error_msg})
            response["metadata"]["stages_failed"] += 1
            raise
        
        # Stage 2: Architect Agent
        logger.info("\n[STAGE 2/5] Starting Technical Architecture Design...")
        try:
            stage_start = time.time()
            architect_result = architect_agent(idea, response["stages"]["business"])
            stage_duration = time.time() - stage_start
            
            if architect_result.get("error"):
                raise Exception(architect_result.get("message", "Architect agent failed"))
            
            response["stages"]["architect"] = architect_result
            response["metadata"]["stages_completed"] += 1
            logger.info(f"✓ Architecture Design completed in {stage_duration:.2f}s")
            
            frontend = architect_result.get('frontend_stack', {})
            backend = architect_result.get('backend_stack', {})
            logger.info(f"  Frontend: {frontend.get('framework', 'N/A')}")
            logger.info(f"  Backend: {backend.get('framework', 'N/A')}")
            
        except Exception as e:
            error_msg = f"Architect Agent failed: {str(e)}"
            logger.error(f"✗ {error_msg}")
            response["errors"].append({"stage": "architect", "error": error_msg})
            response["metadata"]["stages_failed"] += 1
            raise
        
        # Stage 3: Builder Agent
        logger.info("\n[STAGE 3/5] Starting Code Scaffold Generation...")
        try:
            stage_start = time.time()
            builder_result = builder_agent(idea, response["stages"]["architect"])
            stage_duration = time.time() - stage_start
            
            if builder_result.get("error"):
                raise Exception(builder_result.get("message", "Builder agent failed"))
            
            response["stages"]["builder"] = builder_result
            response["metadata"]["stages_completed"] += 1
            
            react_files = len(builder_result.get('react_scaffold', {}))
            fastapi_files = len(builder_result.get('fastapi_scaffold', {}))
            logger.info(f"✓ Code Generation completed in {stage_duration:.2f}s")
            logger.info(f"  React Files: {react_files}")
            logger.info(f"  FastAPI Files: {fastapi_files}")
            
        except Exception as e:
            error_msg = f"Builder Agent failed: {str(e)}"
            logger.error(f"✗ {error_msg}")
            response["errors"].append({"stage": "builder", "error": error_msg})
            response["metadata"]["stages_failed"] += 1
            raise
        
        # Stage 4: Security Agent
        logger.info("\n[STAGE 4/5] Starting Security Review...")
        try:
            stage_start = time.time()
            security_result = security_agent(
                response["stages"]["builder"],
                response["stages"]["architect"]
            )
            stage_duration = time.time() - stage_start
            
            if security_result.get("error"):
                raise Exception(security_result.get("message", "Security agent failed"))
            
            response["stages"]["security"] = security_result
            response["metadata"]["stages_completed"] += 1
            
            security_rating = security_result.get('security_rating', 0)
            severity = security_result.get('severity_summary', {})
            logger.info(f"✓ Security Review completed in {stage_duration:.2f}s")
            logger.info(f"  Security Rating: {security_rating}/100")
            logger.info(f"  Critical Issues: {severity.get('critical', 0)}")
            
            # Check for critical security issues
            if has_critical_issues(security_result):
                logger.warning("⚠ Critical security issues detected!")
                response["errors"].append({
                    "stage": "security",
                    "error": "Critical security issues found",
                    "severity": "critical"
                })
            
        except Exception as e:
            error_msg = f"Security Agent failed: {str(e)}"
            logger.error(f"✗ {error_msg}")
            response["errors"].append({"stage": "security", "error": error_msg})
            response["metadata"]["stages_failed"] += 1
            raise
        
        # Stage 5: GitHub Agent
        logger.info("\n[STAGE 5/5] Starting GitHub Integration Preparation...")
        try:
            stage_start = time.time()
            github_result = github_agent(
                idea,
                response["stages"]["builder"],
                response["stages"]["security"],
                response["stages"]["architect"]
            )
            stage_duration = time.time() - stage_start
            
            if github_result.get("error"):
                raise Exception(github_result.get("message", "GitHub agent failed"))
            
            response["stages"]["github"] = github_result
            response["metadata"]["stages_completed"] += 1
            
            repo = github_result.get('repository_status', {})
            logger.info(f"✓ GitHub Integration completed in {stage_duration:.2f}s")
            logger.info(f"  Repository: {repo.get('name', 'N/A')}")
            
        except Exception as e:
            error_msg = f"GitHub Agent failed: {str(e)}"
            logger.error(f"✗ {error_msg}")
            response["errors"].append({"stage": "github", "error": error_msg})
            response["metadata"]["stages_failed"] += 1
            raise
        
        # Pipeline completed successfully
        response["success"] = True
        end_time = time.time()
        duration = end_time - start_time
        response["metadata"]["end_time"] = datetime.now().isoformat()
        response["metadata"]["duration_seconds"] = round(duration, 2)
        
        logger.info("\n" + "=" * 80)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info(f"Total Duration: {duration:.2f}s")
        logger.info(f"Stages Completed: {response['metadata']['stages_completed']}/5")
        logger.info("=" * 80)
        
        return response
        
    except Exception as e:
        # Pipeline failed
        end_time = time.time()
        duration = end_time - start_time
        response["success"] = False
        response["metadata"]["end_time"] = datetime.now().isoformat()
        response["metadata"]["duration_seconds"] = round(duration, 2)
        
        logger.error("\n" + "=" * 80)
        logger.error("PIPELINE FAILED")
        logger.error(f"Error: {str(e)}")
        logger.error(f"Stages Completed: {response['metadata']['stages_completed']}/5")
        logger.error(f"Stages Failed: {response['metadata']['stages_failed']}")
        logger.error("=" * 80)
        
        # Add general pipeline error if not already added
        if not any(err.get("stage") == "pipeline" for err in response["errors"]):
            response["errors"].append({
                "stage": "pipeline",
                "error": str(e)
            })
        
        return response


# Example usage and testing
if __name__ == "__main__":
    # Test idea
    test_idea = """
    A mobile app that helps busy professionals track their daily water intake.
    Users set hydration goals based on their weight and activity level, and receive
    smart reminders throughout the day. The app integrates with popular fitness trackers
    like Fitbit and Apple Watch to automatically adjust recommendations based on exercise.
    Users can compete with friends through challenges and earn badges for consistency.
    The app also provides personalized insights based on weather conditions and provides
    educational content about the importance of hydration.
    """
    
    print("=" * 60)
    print("AI VENTURE STUDIO - MVP GENERATOR")
    print("=" * 60)
    
    # Validate idea
    print("\n1. Validating idea...")
    validation = validate_idea(test_idea)
    if not validation["valid"]:
        print(f"❌ Validation failed: {validation['error']}")
        exit(1)
    print(f"✓ Idea validated ({validation['word_count']} words)")
    
    # Configure options
    options = {
        "stop_on_critical_security": True,
        "skip_github": False
    }
    
    # Run pipeline
    print("\n2. Starting MVP generation pipeline...")
    print("-" * 60)
    
    result = generate_mvp(test_idea, options)
    
    # Display results
    print("\n" + "=" * 60)
    print(get_pipeline_summary(result))
    print("=" * 60)
    
    # Save outputs if successful
    if result["success"]:
        print("\n3. Saving outputs...")
        
        # Save code scaffold
        if "builder" in result["outputs"]:
            from agents.builder_agent import save_scaffold_to_disk
            saved = save_scaffold_to_disk(result["outputs"]["builder"], "./generated_mvp")
            if "error" not in saved:
                print(f"✓ Code scaffold saved: {len(saved)} files")
        
        # Save GitHub files
        if "github" in result["outputs"]:
            from agents.github_agent import save_github_files
            saved = save_github_files(result["outputs"]["github"], "./generated_mvp")
            if "error" not in saved:
                print(f"✓ GitHub files saved: {len(saved)} files")
        
        print("\n✅ MVP generation complete!")
        print(f"📁 Output directory: ./generated_mvp")
        print(f"⏱️  Total time: {result['metadata']['duration_seconds']}s")
    else:
        print("\n❌ MVP generation failed!")
        print("Errors:")
        for agent, error in result.get("errors", {}).items():
            print(f"  - {agent}: {error}")

# Made with Bob
