"""
Test script for orchestrator.py refactoring
Tests the run_pipeline function with mock mode
"""

import asyncio
import json
from orchestrator import run_pipeline, validate_idea


async def test_mock_mode():
    """Test run_pipeline in mock mode"""
    print("=" * 80)
    print("Testing run_pipeline with live_mode=False (Mock Mode)")
    print("=" * 80)
    
    test_idea = "A mobile app for tracking daily water intake with smart reminders"
    
    # Validate idea first
    print("\n1. Validating idea...")
    validation = validate_idea(test_idea)
    print(f"   Validation result: {validation}")
    
    if not validation["valid"]:
        print(f"   [X] Validation failed: {validation['error']}")
        return
    
    print("   [OK] Idea validated")
    
    # Run pipeline in mock mode
    print("\n2. Running pipeline in mock mode...")
    result = await run_pipeline(test_idea, live_mode=False)
    
    # Display results
    print("\n3. Pipeline Results:")
    print(f"   Success: {result['success']}")
    print(f"   Live Mode: {result['live_mode']}")
    print(f"   Stages Completed: {result['metadata']['stages_completed']}")
    print(f"   Duration: {result['metadata']['duration_seconds']}s")
    print(f"   Errors: {len(result['errors'])}")
    
    print("\n4. Stage Results:")
    for stage_name, stage_result in result['stages'].items():
        if stage_result:
            print(f"   [OK] {stage_name}: {stage_result}")
    
    print("\n5. Full Response (JSON):")
    print(json.dumps(result, indent=2))
    
    print("\n" + "=" * 80)
    if result['success']:
        print("[PASS] TEST PASSED: Mock mode working correctly")
    else:
        print("[FAIL] TEST FAILED: Mock mode returned failure")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_mock_mode())

# Made with Bob
