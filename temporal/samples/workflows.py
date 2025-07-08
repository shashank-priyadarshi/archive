from datetime import timedelta
from typing import Dict, List
from temporalio import workflow
from temporalio.common import RetryPolicy
from .activities import FileProcessingActivities

@workflow.defn
class FileProcessingSagaWorkflow:
    def __init__(self):
        self.activities = FileProcessingActivities()
        self.compensation_steps = []
        self.processing_state = {}

    @workflow.run
    async def run(self, input_data: Dict) -> Dict:
        workflow.logger.info(f"Starting file processing saga for: {input_data}")

        try:
            self.processing_state["workflow_id"] = workflow.info().workflow_id
            self.processing_state["start_time"] = workflow.now().isoformat()

            download_result = await self._download_file_step(input_data)
            validation_result = await self._validate_file_step(download_result)
            backup_result = await self._backup_file_step(validation_result)
            parsing_result = await self._parse_file_step(validation_result)
            processing_result = await self._process_data_step(parsing_result)
            saving_result = await self._save_data_step(processing_result)
            upload_result = await self._upload_data_step(saving_result)
            validation_final = await self._validate_result_step(processing_result)
            notification_result = await self._send_notification_step(upload_result)
            cleanup_result = await self._cleanup_step([download_result["file_path"]])

            await self._log_success_event()

            return {
                "status": "completed",
                "workflow_id": workflow.info().workflow_id,
                "download_result": download_result,
                "validation_result": validation_result,
                "backup_result": backup_result,
                "parsing_result": parsing_result,
                "processing_result": processing_result,
                "saving_result": saving_result,
                "upload_result": upload_result,
                "validation_final": validation_final,
                "notification_result": notification_result,
                "cleanup_result": cleanup_result,
                "compensation_steps": self.compensation_steps
            }

        except Exception as e:
            workflow.logger.error(f"Saga failed: {str(e)}")
            await self._execute_compensation()
            await self._log_failure_event(str(e))
            raise

    async def _download_file_step(self, input_data: Dict) -> Dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=30),
            maximum_attempts=3
        )

        result = await workflow.execute_activity(
            self.activities.download_file,
            input_data["file_url"],
            input_data["filename"],
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=retry_policy
        )

        self.processing_state["download_result"] = result
        self.compensation_steps.append(("cleanup_download", result["file_path"]))

        return result

    async def _validate_file_step(self, download_result: Dict) -> Dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10),
            maximum_attempts=2
        )

        result = await workflow.execute_activity(
            self.activities.validate_file_format,
            download_result["file_path"],
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=retry_policy
        )

        self.processing_state["validation_result"] = result
        return result

    async def _backup_file_step(self, validation_result: Dict) -> Dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10),
            maximum_attempts=3
        )

        result = await workflow.execute_activity(
            self.activities.backup_file,
            self.processing_state["download_result"]["file_path"],
            start_to_close_timeout=timedelta(minutes=3),
            retry_policy=retry_policy
        )

        self.processing_state["backup_result"] = result
        return result

    async def _parse_file_step(self, validation_result: Dict) -> Dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=15),
            maximum_attempts=2
        )

        result = await workflow.execute_activity(
            self.activities.parse_file_content,
            self.processing_state["download_result"]["file_path"],
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=retry_policy
        )

        self.processing_state["parsing_result"] = result
        return result

    async def _process_data_step(self, parsing_result: Dict) -> Dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            maximum_interval=timedelta(seconds=30),
            maximum_attempts=3
        )

        result = await workflow.execute_activity(
            self.activities.process_data_records,
            parsing_result,
            start_to_close_timeout=timedelta(minutes=10),
            retry_policy=retry_policy
        )

        self.processing_state["processing_result"] = result
        return result

    async def _save_data_step(self, processing_result: Dict) -> Dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10),
            maximum_attempts=3
        )

        output_filename = f"processed_{workflow.info().workflow_id}.json"
        result = await workflow.execute_activity(
            self.activities.save_processed_data,
            processing_result,
            output_filename,
            start_to_close_timeout=timedelta(minutes=3),
            retry_policy=retry_policy
        )

        self.processing_state["saving_result"] = result
        self.compensation_steps.append(("cleanup_saved", result["output_path"]))

        return result

    async def _upload_data_step(self, saving_result: Dict) -> Dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=5),
            maximum_interval=timedelta(seconds=60),
            maximum_attempts=3
        )

        result = await workflow.execute_activity(
            self.activities.upload_to_external_service,
            saving_result["output_path"],
            "http://localhost:8080/upload",
            start_to_close_timeout=timedelta(minutes=15),
            retry_policy=retry_policy
        )

        self.processing_state["upload_result"] = result
        self.compensation_steps.append(("rollback_upload", result["upload_id"]))

        return result

    async def _validate_result_step(self, processing_result: Dict) -> Dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10),
            maximum_attempts=2
        )

        result = await workflow.execute_activity(
            self.activities.validate_processing_result,
            processing_result,
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=retry_policy
        )

        self.processing_state["validation_final"] = result
        return result

    async def _send_notification_step(self, upload_result: Dict) -> Dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            maximum_interval=timedelta(seconds=30),
            maximum_attempts=3
        )

        message = f"File processing completed successfully. Upload ID: {upload_result['upload_id']}"
        result = await workflow.execute_activity(
            self.activities.send_notification,
            message,
            "http://localhost:8080/webhook",
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=retry_policy
        )

        self.processing_state["notification_result"] = result
        return result

    async def _cleanup_step(self, file_paths: List[str]) -> Dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10),
            maximum_attempts=2
        )

        result = await workflow.execute_activity(
            self.activities.cleanup_temp_files,
            file_paths,
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=retry_policy
        )

        self.processing_state["cleanup_result"] = result
        return result

    async def _execute_compensation(self):
        workflow.logger.info("Executing compensation steps")

        for step_type, step_data in reversed(self.compensation_steps):
            try:
                if step_type == "cleanup_download":
                    await workflow.execute_activity(
                        self.activities.cleanup_temp_files,
                        [step_data],
                        start_to_close_timeout=timedelta(minutes=1)
                    )
                elif step_type == "cleanup_saved":
                    await workflow.execute_activity(
                        self.activities.cleanup_temp_files,
                        [step_data],
                        start_to_close_timeout=timedelta(minutes=1)
                    )
                elif step_type == "rollback_upload":
                    await workflow.execute_activity(
                        self.activities.rollback_upload,
                        step_data,
                        "http://localhost:8080",
                        start_to_close_timeout=timedelta(minutes=5)
                    )

            except Exception as e:
                workflow.logger.error(f"Compensation step {step_type} failed: {str(e)}")

    async def _log_success_event(self):
        event_data = {
            "event_type": "saga_completed",
            "workflow_id": workflow.info().workflow_id,
            "status": "success",
            "processing_state": self.processing_state
        }

        await workflow.execute_activity(
            self.activities.log_processing_event,
            event_data,
            start_to_close_timeout=timedelta(minutes=1)
        )

    async def _log_failure_event(self, error_message: str):
        event_data = {
            "event_type": "saga_failed",
            "workflow_id": workflow.info().workflow_id,
            "status": "failed",
            "error": error_message,
            "processing_state": self.processing_state
        }

        await workflow.execute_activity(
            self.activities.log_processing_event,
            event_data,
            start_to_close_timeout=timedelta(minutes=1)
        )

@workflow.defn
class SimpleFileProcessingWorkflow:
    def __init__(self):
        self.activities = FileProcessingActivities()

    @workflow.run
    async def run(self, file_url: str, filename: str) -> Dict:
        download_result = await workflow.execute_activity(
            self.activities.download_file,
            file_url,
            filename,
            start_to_close_timeout=timedelta(minutes=5)
        )

        validation_result = await workflow.execute_activity(
            self.activities.validate_file_format,
            download_result["file_path"],
            start_to_close_timeout=timedelta(minutes=2)
        )

        parsing_result = await workflow.execute_activity(
            self.activities.parse_file_content,
            download_result["file_path"],
            start_to_close_timeout=timedelta(minutes=5)
        )

        processing_result = await workflow.execute_activity(
            self.activities.process_data_records,
            parsing_result,
            start_to_close_timeout=timedelta(minutes=10)
        )

        output_filename = f"simple_processed_{workflow.info().workflow_id}.json"
        saving_result = await workflow.execute_activity(
            self.activities.save_processed_data,
            processing_result,
            output_filename,
            start_to_close_timeout=timedelta(minutes=3)
        )

        await workflow.execute_activity(
            self.activities.cleanup_temp_files,
            [download_result["file_path"]],
            start_to_close_timeout=timedelta(minutes=1)
        )

        return {
            "status": "completed",
            "download_result": download_result,
            "validation_result": validation_result,
            "parsing_result": parsing_result,
            "processing_result": processing_result,
            "saving_result": saving_result
        }
