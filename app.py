from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import uuid
from telemetry import create_telemetry_logger
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Initialize telemetry
telemetry = create_telemetry_logger("addition-service")
logger = telemetry.get_logger()

# Response model for API documentation
class AdditionResult(BaseModel):
    result: float
    operation: str = "addition"
    first_number: float
    second_number: float

class HealthCheck(BaseModel):
    status: str
    service: str

def addition(firstNumber: float, secondNumber: float) -> float:
    """Perform addition of two numbers."""
    # Start trace
    trace_id = str(uuid.uuid4())
    span_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        result = firstNumber + secondNumber
        duration_ms = (time.time() - start_time) * 1000
        
        # Log successful operation
        logger.info(f"Addition performed: {firstNumber} + {secondNumber} = {result}")
        
        # Log trace
        telemetry.log_trace(
            trace_id=trace_id,
            span_id=span_id,
            operation="addition",
            duration_ms=duration_ms,
            metadata={
                "first_number": firstNumber,
                "second_number": secondNumber,
                "result": result
            }
        )
        
        # Log metrics
        telemetry.log_metrics({
            "operation": "addition",
            "success": True,
            "response_time_ms": duration_ms
        })
        
        return result
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        telemetry.log_error_with_trace(e, {
            "operation": "addition",
            "first_number": firstNumber,
            "second_number": secondNumber,
            "duration_ms": duration_ms
        })
        raise


app = FastAPI(
    title="Addition Service",
    description="Microservice for performing addition operations",
    version="1.0.0"
)
FastAPIInstrumentor().instrument_app(app)

@app.get("/health", response_model=HealthCheck, tags=["health"])
async def health_check():
    """Health check endpoint to verify service is running."""
    logger.info("Health check requested")
    telemetry.log_metrics({
        "health_check": 1,
        "service": "addition-service",
        "status": "healthy"
    })
    return {"status": "healthy", "service": "addition-service"}

@app.get("/", response_model=AdditionResult, tags=["operations"])
async def add_numbers(
    first_number: float = 0, 
    second_number: float = 0
) -> AdditionResult:
    """
    Add two numbers together.
    
    - **first_number**: The first number to add
    - **second_number**: The second number to add
    
    Returns the sum of the two numbers.
    """
    try:
        result = addition(first_number, second_number)
        return AdditionResult(
            result=result,
            first_number=first_number,
            second_number=second_number
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
