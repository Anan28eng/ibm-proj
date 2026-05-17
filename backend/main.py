from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Optional

# Import the orchestrator function
try:
    from orchestrator import run_pipeline
except ImportError:
    # Fallback if orchestrator is in a different location
    from backend.orchestrator import run_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered SaaS Generator API",
    description="Backend API for generating SaaS applications from ideas",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this based on your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class GenerateRequest(BaseModel):
    idea: str
    live_mode: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "idea": "A task management app with AI-powered prioritization",
                "live_mode": False
            }
        }


# Health check endpoint
@app.get("/")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status message
    """
    return {
        "status": "healthy",
        "message": "AI-Powered SaaS Generator API is running",
        "version": "1.0.0"
    }


# Generate endpoint
@app.post("/generate")
async def generate(request: GenerateRequest):
    """
    Generate a SaaS application from an idea.
    
    Args:
        request: GenerateRequest containing the idea and live_mode flag
        
    Returns:
        dict: Result from the pipeline execution
        
    Raises:
        HTTPException: If pipeline execution fails
    """
    try:
        logger.info(f"Received generation request for idea: {request.idea[:50]}...")
        logger.info(f"Live mode: {request.live_mode}")
        
        # Validate input
        if not request.idea or len(request.idea.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Idea cannot be empty"
            )
        
        # Call the orchestrator pipeline
        result = await run_pipeline(
            idea=request.idea,
            live_mode=request.live_mode
        )
        
        logger.info("Pipeline execution completed successfully")
        
        return {
            "success": True,
            "message": "SaaS application generated successfully",
            "data": result
        }
        
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(ve)}"
        )
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate SaaS application: {str(e)}"
        )


# Optional: Add startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup.
    """
    logger.info("Starting AI-Powered SaaS Generator API...")
    logger.info("API is ready to accept requests")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown.
    """
    logger.info("Shutting down AI-Powered SaaS Generator API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

# Made with Bob
