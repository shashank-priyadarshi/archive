import pytest
import asyncio
import tempfile
import os
import json
from unittest.mock import patch, Mock, AsyncMock
from temporalio.testing import WorkflowEnvironment
from temporalio.client import Client
from temporalio.worker import Worker
from activities import FileProcessingActivities
from workflows import FileProcessingSagaWorkflow, SimpleFileProcessingWorkflow

@pytest.fixture
async def temporal_environment():
    async with WorkflowEnvironment.start_local() as env:
        client = await env.client()

        activities_instance = FileProcessingActivities()

        worker = Worker(
            client,
            task_queue="test-queue",
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

        worker_task = asyncio.create_task(worker.run())

        yield client, worker

        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass
        await env.shutdown()

@pytest.fixture
def sample_json_data():
    return [
        {"id": 1, "title": "Test Post 1", "body": "Test content 1"},
        {"id": 2, "title": "Test Post 2", "body": "Test content 2"},
        {"id": 3, "title": "Test Post 3", "body": "Test content 3"}
    ]

@pytest.fixture
def sample_csv_data():
    return "id,name,email\n1,John Doe,john@example.com\n2,Jane Smith,jane@example.com"

class TestFileProcessingActivities:
    def test_activity_initialization(self):
        activities = FileProcessingActivities()
        assert activities.base_path == "/tmp/temporal_processing"
        assert os.path.exists(activities.base_path)

    @patch('aiohttp.ClientSession')
    async def test_download_file_success(self, mock_session):
        activities = FileProcessingActivities()

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"test": "data"}'

        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response

        result = await activities.download_file("https://example.com/test.json", "test.json")

        assert result["success"] is True
        assert "file_path" in result
        assert result["size"] > 0

    @patch('aiohttp.ClientSession')
    async def test_download_file_failure(self, mock_session):
        activities = FileProcessingActivities()

        mock_response = AsyncMock()
        mock_response.status = 404

        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value = mock_response

        with pytest.raises(Exception, match="Failed to download file: 404"):
            await activities.download_file("https://example.com/notfound.json", "notfound.json")

    async def test_validate_file_format_success(self):
        activities = FileProcessingActivities()

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            f.write(b'{"test": "data"}')
            temp_file = f.name

        try:
            result = await activities.validate_file_format(temp_file)
            assert result["success"] is True
            assert result["valid"] is True
            assert result["file_type"] == ".json"
        finally:
            os.unlink(temp_file)

    async def test_validate_file_format_empty_file(self):
        activities = FileProcessingActivities()

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            with pytest.raises(Exception, match="File is empty"):
                await activities.validate_file_format(temp_file)
        finally:
            os.unlink(temp_file)

    async def test_parse_file_content_json(self, sample_json_data):
        activities = FileProcessingActivities()

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            json.dump(sample_json_data, f)
            temp_file = f.name

        try:
            result = await activities.parse_file_content(temp_file)
            assert result["success"] is True
            assert result["file_type"] == "json"
            assert result["records_count"] == 3
            assert len(result["parsed_data"]) == 3
        finally:
            os.unlink(temp_file)

    async def test_parse_file_content_csv(self, sample_csv_data):
        activities = FileProcessingActivities()

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            f.write(sample_csv_data.encode())
            temp_file = f.name

        try:
            result = await activities.parse_file_content(temp_file)
            assert result["success"] is True
            assert result["file_type"] == "csv"
            assert result["records_count"] == 2
        finally:
            os.unlink(temp_file)

    async def test_process_data_records_json(self, sample_json_data):
        activities = FileProcessingActivities()

        parsed_data = {
            "success": True,
            "records_count": 3,
            "parsed_data": sample_json_data,
            "file_type": "json"
        }

        result = await activities.process_data_records(parsed_data)
        assert result["success"] is True
        assert result["processed_count"] == 3
        assert len(result["processed_records"]) == 3

    async def test_save_processed_data(self):
        activities = FileProcessingActivities()

        processed_data = {
            "success": True,
            "processed_count": 2,
            "processed_records": [
                {"id": "1", "data": {"test": "data1"}},
                {"id": "2", "data": {"test": "data2"}}
            ]
        }

        result = await activities.save_processed_data(processed_data, "test_output.json")
        assert result["success"] is True
        assert result["records_saved"] == 2
        assert os.path.exists(result["output_path"])

class TestWorkflows:
    async def test_simple_workflow_success(self, temporal_environment):
        client, worker = temporal_environment

        with patch('activities.FileProcessingActivities.download_file') as mock_download, \
             patch('activities.FileProcessingActivities.validate_file_format') as mock_validate, \
             patch('activities.FileProcessingActivities.parse_file_content') as mock_parse, \
             patch('activities.FileProcessingActivities.process_data_records') as mock_process, \
             patch('activities.FileProcessingActivities.save_processed_data') as mock_save, \
             patch('activities.FileProcessingActivities.cleanup_temp_files') as mock_cleanup:

            mock_download.return_value = {
                "success": True,
                "file_path": "/tmp/test.json",
                "size": 100
            }

            mock_validate.return_value = {
                "success": True,
                "file_size": 100,
                "file_type": ".json",
                "valid": True
            }

            mock_parse.return_value = {
                "success": True,
                "records_count": 2,
                "parsed_data": [{"id": 1}, {"id": 2}],
                "file_type": "json"
            }

            mock_process.return_value = {
                "success": True,
                "processed_count": 2,
                "processed_records": [{"id": "1"}, {"id": "2"}]
            }

            mock_save.return_value = {
                "success": True,
                "output_path": "/tmp/output.json",
                "output_size": 200,
                "records_saved": 2
            }

            mock_cleanup.return_value = {
                "success": True,
                "cleaned_files": ["/tmp/test.json"],
                "failed_files": [],
                "total_cleaned": 1
            }

            result = await client.execute_workflow(
                SimpleFileProcessingWorkflow.run,
                "https://example.com/test.json",
                "test.json",
                id="test-simple-workflow",
                task_queue="test-queue"
            )

            assert result["status"] == "completed"
            assert "download_result" in result
            assert "validation_result" in result
            assert "parsing_result" in result
            assert "processing_result" in result
            assert "saving_result" in result

    async def test_saga_workflow_success(self, temporal_environment):
        client, worker = temporal_environment

        with patch('activities.FileProcessingActivities.download_file') as mock_download, \
             patch('activities.FileProcessingActivities.validate_file_format') as mock_validate, \
             patch('activities.FileProcessingActivities.backup_file') as mock_backup, \
             patch('activities.FileProcessingActivities.parse_file_content') as mock_parse, \
             patch('activities.FileProcessingActivities.process_data_records') as mock_process, \
             patch('activities.FileProcessingActivities.save_processed_data') as mock_save, \
             patch('activities.FileProcessingActivities.upload_to_external_service') as mock_upload, \
             patch('activities.FileProcessingActivities.validate_processing_result') as mock_validate_result, \
             patch('activities.FileProcessingActivities.send_notification') as mock_notification, \
             patch('activities.FileProcessingActivities.cleanup_temp_files') as mock_cleanup, \
             patch('activities.FileProcessingActivities.log_processing_event') as mock_log:

            mock_download.return_value = {
                "success": True,
                "file_path": "/tmp/test.json",
                "size": 100
            }

            mock_validate.return_value = {
                "success": True,
                "file_size": 100,
                "file_type": ".json",
                "valid": True
            }

            mock_backup.return_value = {
                "success": True,
                "original_path": "/tmp/test.json",
                "backup_path": "/tmp/backup/test.json",
                "backup_size": 100
            }

            mock_parse.return_value = {
                "success": True,
                "records_count": 2,
                "parsed_data": [{"id": 1}, {"id": 2}],
                "file_type": "json"
            }

            mock_process.return_value = {
                "success": True,
                "processed_count": 2,
                "processed_records": [{"id": "1"}, {"id": "2"}]
            }

            mock_save.return_value = {
                "success": True,
                "output_path": "/tmp/output.json",
                "output_size": 200,
                "records_saved": 2
            }

            mock_upload.return_value = {
                "success": True,
                "upload_id": "upload_123",
                "service_response": {"status": "success"},
                "uploaded_at": "2024-01-01T00:00:00"
            }

            mock_validate_result.return_value = {
                "success": True,
                "validation_passed": True,
                "records_validated": 2,
                "validation_timestamp": "2024-01-01T00:00:00"
            }

            mock_notification.return_value = {
                "success": True,
                "notification_sent": True,
                "response_status": 200
            }

            mock_cleanup.return_value = {
                "success": True,
                "cleaned_files": ["/tmp/test.json"],
                "failed_files": [],
                "total_cleaned": 1
            }

            mock_log.return_value = {
                "success": True,
                "log_file": "/tmp/log.txt",
                "logged_at": "2024-01-01T00:00:00"
            }

            input_data = {
                "file_url": "https://example.com/test.json",
                "filename": "test.json"
            }

            result = await client.execute_workflow(
                FileProcessingSagaWorkflow.run,
                input_data,
                id="test-saga-workflow",
                task_queue="test-queue"
            )

            assert result["status"] == "completed"
            assert "download_result" in result
            assert "backup_result" in result
            assert "upload_result" in result
            assert "compensation_steps" in result

    async def test_saga_workflow_compensation(self, temporal_environment):
        client, worker = temporal_environment

        with patch('activities.FileProcessingActivities.download_file') as mock_download, \
             patch('activities.FileProcessingActivities.validate_file_format') as mock_validate, \
             patch('activities.FileProcessingActivities.upload_to_external_service') as mock_upload, \
             patch('activities.FileProcessingActivities.rollback_upload') as mock_rollback, \
             patch('activities.FileProcessingActivities.cleanup_temp_files') as mock_cleanup, \
             patch('activities.FileProcessingActivities.log_processing_event') as mock_log:

            mock_download.return_value = {
                "success": True,
                "file_path": "/tmp/test.json",
                "size": 100
            }

            mock_validate.return_value = {
                "success": True,
                "file_size": 100,
                "file_type": ".json",
                "valid": True
            }

            mock_upload.side_effect = Exception("Upload failed")

            mock_rollback.return_value = {
                "success": True,
                "rollback_id": "upload_123",
                "rollback_status": "completed"
            }

            mock_cleanup.return_value = {
                "success": True,
                "cleaned_files": ["/tmp/test.json"],
                "failed_files": [],
                "total_cleaned": 1
            }

            mock_log.return_value = {
                "success": True,
                "log_file": "/tmp/log.txt",
                "logged_at": "2024-01-01T00:00:00"
            }

            input_data = {
                "file_url": "https://example.com/test.json",
                "filename": "test.json"
            }

            with pytest.raises(Exception):
                await client.execute_workflow(
                    FileProcessingSagaWorkflow.run,
                    input_data,
                    id="test-saga-compensation",
                    task_queue="test-queue"
                )

if __name__ == "__main__":
    pytest.main([__file__])
