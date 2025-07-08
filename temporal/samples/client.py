import asyncio
import json
import logging
from temporalio.client import Client
from workflows import FileProcessingSagaWorkflow, SimpleFileProcessingWorkflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_saga_workflow():
    client = await Client.connect("localhost:7233")

    input_data = {
        "file_url": "http://localhost:8080/sample-data/posts",
        "filename": "posts.json"
    }

    logger.info("Starting Saga workflow...")

    result = await client.execute_workflow(
        FileProcessingSagaWorkflow.run,
        input_data,
        id="saga-workflow-demo",
        task_queue="file-processing-queue"
    )

    logger.info(f"Saga workflow completed: {result['status']}")
    return result

async def run_simple_workflow():
    client = await Client.connect("localhost:7233")

    logger.info("Starting simple workflow...")

    result = await client.execute_workflow(
        SimpleFileProcessingWorkflow.run,
        "http://localhost:8080/sample-data/users",
        "users.json",
        id="simple-workflow-demo",
        task_queue="file-processing-queue"
    )

    logger.info(f"Simple workflow completed: {result['status']}")
    return result

async def run_workflow_with_signals():
    client = await Client.connect("localhost:7233")

    input_data = {
        "file_url": "http://localhost:8080/sample-data/albums",
        "filename": "albums.json"
    }

    logger.info("Starting workflow with signal handling...")

    handle = await client.start_workflow(
        FileProcessingSagaWorkflow.run,
        input_data,
        id="signal-workflow-demo",
        task_queue="file-processing-queue"
    )

    logger.info(f"Workflow started with ID: {handle.id}")

    try:
        result = await handle.result(timeout=300)
        logger.info(f"Workflow completed: {result['status']}")
        return result
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        raise

async def query_workflow_status(workflow_id: str):
    client = await Client.connect("localhost:7233")

    handle = client.get_workflow_handle(workflow_id)

    try:
        desc = await handle.describe()
        logger.info(f"Workflow {workflow_id} status: {desc.status.name}")
        return desc
    except Exception as e:
        logger.error(f"Failed to query workflow: {e}")
        raise

async def cancel_workflow(workflow_id: str):
    client = await Client.connect("localhost:7233")

    handle = client.get_workflow_handle(workflow_id)

    try:
        await handle.cancel()
        logger.info(f"Workflow {workflow_id} cancelled")
    except Exception as e:
        logger.error(f"Failed to cancel workflow: {e}")
        raise

async def main():
    try:
        logger.info("Running Temporal file processing workflows...")

        saga_result = await run_saga_workflow()
        print(json.dumps(saga_result, indent=2))

        simple_result = await run_simple_workflow()
        print(json.dumps(simple_result, indent=2))

        signal_result = await run_workflow_with_signals()
        print(json.dumps(signal_result, indent=2))

    except Exception as e:
        logger.error(f"Error running workflows: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
