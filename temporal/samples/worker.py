import asyncio
import logging
import os
import signal
import sys
from temporalio.client import Client
from temporalio.worker import Worker
from activities import FileProcessingActivities
from workflows import FileProcessingSagaWorkflow, SimpleFileProcessingWorkflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    client = await Client.connect("localhost:7233")

    activities_instance = FileProcessingActivities()

    worker = Worker(
        client,
        task_queue="file-processing-queue",
        workflows=[FileProcessingSagaWorkflow, SimpleFileProcessingWorkflow],
        activities=[
            activities_instance.download_file,
            activities_instance.validate_file_format,
            activities_instance.parse_file_content,
            activities_instance.backup_file,
            activities_instance.process_data_records,
            activities_instance.save_processed_data,
            activities_instance.upload_to_external_service,
            activities_instance.send_notification,
            activities_instance.cleanup_temp_files,
            activities_instance.log_processing_event,
            activities_instance.rollback_upload,
            activities_instance.restore_from_backup,
            activities_instance.validate_processing_result
        ]
    )

    logger.info("Starting Temporal worker for file processing...")
    await worker.run()

def signal_handler(signum, frame):
    logger.info("Received shutdown signal, stopping worker...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Worker stopped by user")
    except Exception as e:
        logger.error(f"Worker failed: {e}")
        sys.exit(1)
