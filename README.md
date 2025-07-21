# Addition Service

A microservice that performs addition operations as part of the [Useless Calculator](https://github.com/solvedevops/useless-calculator) project.

**⚠️ DEMO PROJECT WARNING**: This service is designed for demonstration and training purposes only. It should **NOT** be used in production environments. You have been warned!

## 🧮 Functionality

This service provides a simple REST API for adding two numbers together.

### Endpoint

- **GET** `/` - Perform addition operation
  - **Parameters:**
    - `first_number` (float, optional): First number to add (default: 0)
    - `second_number` (float, optional): Second number to add (default: 0)
  - **Returns:** JSON object with operation result

- **GET** `/health` - Health check endpoint
  - **Returns:** Service health status

## 🛠️ Technology Stack

- **FastAPI** - Modern Python web framework
- **Python 3.7+** - Programming language
- **Pydantic** - Data validation and serialization
- **Docker** - Containerization

## 🚀 Quick Start

### Using Docker

```bash
# Build and run
docker build -t addition-service .
docker run -p 5001:5001 \
  -e ENV_NAME=development \
  -e APP_NAME=addition-service \
  -e TELEMETRY_MODE=console \
  addition-service
```

### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export ENV_NAME=development
   export APP_NAME=addition-service
   export TELEMETRY_MODE=console
   ```

3. **Run the service:**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 5001
   ```

## Container tags
In order to keep the containers small, the default tag :latest includes only local and console storage for logs, metrics and traces.
To demo cloud provide storage for logs, metrics and traces use the following tags. You still have to pass the TELEMETRY_MODE= env variable

- :latest for console and local storage
- :aws-logs for cloudwatch configuration (You need IAM for this to work)
- :azure-logs for Azure monitor (You need connection string for Azure monitor for this to work)

## ⚙️ Configuration

### Required Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENV_NAME` | Yes | `development` | Environment identifier |
| `APP_NAME` | Yes | `addition-service` | Application identifier |

### Telemetry Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEMETRY_MODE` | No | `console` | Logging destination |
| `AWS_DEFAULT_REGION` | CloudWatch | `us-east-1` | AWS region for CloudWatch |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | Azure | None | Azure Monitor connection |

#### Telemetry Modes

```bash
# Console output (default)
TELEMETRY_MODE=console

# Local file logging (structured: logs/env/app/service/)
TELEMETRY_MODE=local

# AWS CloudWatch (creates: /env/app/logs, /env/app/metrics, /env/app/traces)
TELEMETRY_MODE=aws_cloudwatch

# Azure Monitor (structured with env.app namespace)
TELEMETRY_MODE=azure_monitor

# Multiple outputs
TELEMETRY_MODE=console,local
```

## 📊 API Documentation

### Addition Operation

**Request:**
```bash
GET /?first_number=5&second_number=3
```

**Response:**
```json
{
  "result": 8.0,
  "operation": "addition",
  "first_number": 5.0,
  "second_number": 3.0
}
```

### Health Check

**Request:**
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "addition-service"
}
```

### Interactive API Documentation

When running the service, access:
- **Swagger UI**: http://localhost:5001/docs
- **ReDoc**: http://localhost:5001/redoc

## 📈 Monitoring & Observability

### Structured Telemetry

The service provides comprehensive observability:

- **Logs**: Operation events and errors
- **Metrics**: Performance metrics with response times
- **Traces**: Request tracing with operation details

#### Cloud Integration

**AWS CloudWatch:**
- Log Groups: `/{ENV_NAME}/{APP_NAME}/{logs|metrics|traces}`
- Log Streams: `addition-service/{HOSTNAME}/{YYYY/MM/DD}`

**Azure Monitor:**
- Namespace: `{ENV_NAME}.{APP_NAME}`
- Service: `addition-service`
- Types: logs, metrics, traces

### Example Telemetry Output

**Metrics:**
```json
{
  "operation": "addition",
  "success": true,
  "response_time_ms": 15.3,
  "env_name": "production",
  "app_name": "addition-service",
  "service_name": "addition-service"
}
```

**Traces:**
```json
{
  "trace_id": "abc-123",
  "span_id": "def-456",
  "operation": "addition",
  "duration_ms": 15.3,
  "metadata": {
    "first_number": 5.0,
    "second_number": 3.0,
    "result": 8.0
  }
}
```

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest test_app.py -v
```

### Test Examples

```bash
# Test basic addition
curl "http://localhost:5001/?first_number=10&second_number=5"
# Expected: {"result": 15.0, "operation": "addition", ...}

# Test with decimals
curl "http://localhost:5001/?first_number=7.5&second_number=2.5"
# Expected: {"result": 10.0, "operation": "addition", ...}

# Test health check
curl "http://localhost:5001/health"
# Expected: {"status": "healthy", "service": "addition-service"}
```

## 🔧 Development

### Project Structure

```
addition-service/
├── app.py              # FastAPI application
├── telemetry.py        # Telemetry and logging module
├── test_app.py         # Unit tests
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
└── README.md          # This file
```

### Key Features

- ✅ Input validation and type conversion
- ✅ Comprehensive error handling
- ✅ Health check endpoint
- ✅ Structured logging and telemetry
- ✅ API documentation
- ✅ Unit tests
- ✅ Docker support

## 🔐 Security Notes

- No sensitive data is processed or logged
- Input validation prevents basic injection attacks
- Telemetry follows secure logging practices
- Health checks don't expose sensitive information

## 📚 Related Services

- [Main Calculator](https://github.com/solvedevops/useless-calculator) - Web interface and orchestrator
- [Multiplication Service](https://github.com/solvedevops/multiplication-service) - Handles multiplication operations
- [Division Service](https://github.com/solvedevops/division-service) - Handles division operations
- [Subtraction Service](https://github.com/solvedevops/subtraction-service) - Handles subtraction operations  


## ⚖️ License

This project is for educational and demonstration purposes. Use at your own risk in demo environments only. Attributions Welcome!