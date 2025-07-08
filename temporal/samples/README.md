# Temporal File Processing Saga Example

This example demonstrates a comprehensive file processing workflow using Temporal's Saga orchestration pattern with compensation logic for error handling.

## Problem Statement

The example implements a file processing pipeline that:
1. Downloads files from external URLs
2. Validates file formats and content
3. Creates backups before processing
4. Parses and processes data records
5. Saves processed data to local storage
6. Uploads results to external services
7. Sends notifications
8. Cleans up temporary files

The Saga pattern ensures that if any step fails, all previous operations are properly compensated (rolled back).

## Architecture

- **Activities**: Complex file and network I/O operations organized in a class
- **Workflows**: Two workflow types - a comprehensive Saga workflow and a simple workflow
- **Worker**: Separate worker process that handles task execution
- **Client**: Example client for starting and monitoring workflows
- **Sample Server**: Local server providing sample data and API endpoints

## Data Directories

The example creates two main data directories:
- `temporal_processing_data/` - Files created by activities (input, processed, backup, logs)
- `temporal_samples_data/` - Files managed by the sample server (uploads, webhook logs)

## Files

- `activities.py` - File processing activities with network and file I/O
- `workflows.py` - Saga orchestration workflows with compensation logic
- `worker.py` - Temporal worker main process
- `client.py` - Example client for running workflows
- `sample_server.py` - Local server providing sample data and endpoints
- `start_all.py` - Automated startup script for all components
- `test_workflows.py` - Comprehensive test suite
- `requirements.txt` - Python dependencies

## Setup

### Option 1: Automated Setup (Recommended)
Run the startup script to launch all components automatically:
```bash
python start_all.py
```

### Option 2: Manual Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Temporal server:
```bash
docker run --rm -p 7233:7233 temporalio/auto-setup:1.22.0
```

3. Start the sample server (in a new terminal):
```bash
python sample_server.py
```

4. Start the worker (in another terminal):
```bash
python worker.py
```

5. Run the client (in another terminal):
```bash
python client.py
```

## Running Tests

```bash
pytest test_workflows.py -v
```

## Key Features

- **Saga Pattern**: Complete compensation logic for rollback scenarios
- **Complex I/O**: File operations, HTTP requests, data processing
- **Error Handling**: Comprehensive retry policies and error recovery
- **Monitoring**: Logging and event tracking throughout the process
- **Testing**: Unit and integration tests with mocked dependencies

## Workflow Types

### FileProcessingSagaWorkflow
Complete Saga workflow with:
- Download → Validate → Backup → Parse → Process → Save → Upload → Validate → Notify → Cleanup
- Compensation steps for rollback scenarios
- Comprehensive error handling and logging

### SimpleFileProcessingWorkflow
Simplified workflow for basic file processing:
- Download → Validate → Parse → Process → Save → Cleanup

## Activity Operations

- **File Operations**: Download, validate, backup, parse, save, cleanup
- **Network Operations**: HTTP uploads, notifications, rollbacks
- **Data Processing**: Record transformation and validation
- **Logging**: Event tracking and audit trails

## Compensation Logic

The Saga workflow includes compensation steps for:
- File cleanup on download failure
- Upload rollback on processing failure
- Backup restoration on validation failure

This ensures data consistency and proper resource cleanup in failure scenarios.
