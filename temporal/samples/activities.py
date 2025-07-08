import asyncio
import aiohttp
import aiofiles
import json
import os
import tempfile
import shutil
from datetime import datetime
from typing import Dict, List, Optional
from temporalio import activity
import logging

class FileProcessingActivities:
    def __init__(self):
        self.base_path = os.path.join(os.getcwd(), "temporal_processing_data")
        self.ensure_directories()
        logging.info(f"FileProcessingActivities initialized with base path: {self.base_path}")

    def ensure_directories(self):
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(f"{self.base_path}/input", exist_ok=True)
        os.makedirs(f"{self.base_path}/processed", exist_ok=True)
        os.makedirs(f"{self.base_path}/backup", exist_ok=True)
        os.makedirs(f"{self.base_path}/logs", exist_ok=True)
        logging.info(f"Created/verified directories in: {self.base_path}")

    @activity.defn
    async def download_file(self, url: str, filename: str) -> Dict:
        logging.info(f"Downloading file from {url} to {filename}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    file_path = f"{self.base_path}/input/{filename}"
                    async with aiofiles.open(file_path, 'wb') as f:
                        await f.write(await response.read())
                    file_size = os.path.getsize(file_path)
                    logging.info(f"Downloaded file saved to: {file_path} (Size: {file_size} bytes)")
                    return {
                        "success": True,
                        "file_path": file_path,
                        "size": file_size,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    logging.error(f"Download failed with status: {response.status}")
                    raise Exception(f"Failed to download file: {response.status}")

    @activity.defn
    async def validate_file_format(self, file_path: str) -> Dict:
        if not os.path.exists(file_path):
            raise Exception("File does not exist")

        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise Exception("File is empty")

        file_extension = os.path.splitext(file_path)[1].lower()
        valid_extensions = ['.json', '.csv', '.txt', '.xml']

        if file_extension not in valid_extensions:
            raise Exception(f"Unsupported file format: {file_extension}")

        return {
            "success": True,
            "file_size": file_size,
            "file_type": file_extension,
            "valid": True
        }

    @activity.defn
    async def parse_file_content(self, file_path: str) -> Dict:
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.json':
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
                data = json.loads(content)
                return {
                    "success": True,
                    "records_count": len(data) if isinstance(data, list) else 1,
                    "parsed_data": data,
                    "file_type": "json"
                }
        elif file_extension == '.csv':
            async with aiofiles.open(file_path, 'r') as f:
                lines = await f.readlines()
                records = [line.strip().split(',') for line in lines if line.strip()]
                return {
                    "success": True,
                    "records_count": len(records),
                    "parsed_data": records,
                    "file_type": "csv"
                }
        else:
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
                return {
                    "success": True,
                    "records_count": len(content.split('\n')),
                    "parsed_data": content,
                    "file_type": "text"
                }

    @activity.defn
    async def backup_file(self, file_path: str) -> Dict:
        filename = os.path.basename(file_path)
        backup_path = f"{self.base_path}/backup/{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        shutil.copy2(file_path, backup_path)

        return {
            "success": True,
            "original_path": file_path,
            "backup_path": backup_path,
            "backup_size": os.path.getsize(backup_path)
        }

    @activity.defn
    async def process_data_records(self, parsed_data: Dict) -> Dict:
        if parsed_data["file_type"] == "json":
            processed_records = []
            for record in parsed_data["parsed_data"]:
                if isinstance(record, dict):
                    processed_record = {
                        "id": record.get("id", f"gen_{len(processed_records)}"),
                        "processed_at": datetime.now().isoformat(),
                        "data": record,
                        "status": "processed"
                    }
                    processed_records.append(processed_record)

            return {
                "success": True,
                "processed_count": len(processed_records),
                "processed_records": processed_records
            }
        else:
            processed_records = []
            for i, record in enumerate(parsed_data["parsed_data"]):
                processed_record = {
                    "id": f"record_{i}",
                    "processed_at": datetime.now().isoformat(),
                    "data": record,
                    "status": "processed"
                }
                processed_records.append(processed_record)

            return {
                "success": True,
                "processed_count": len(processed_records),
                "processed_records": processed_records
            }

    @activity.defn
    async def save_processed_data(self, processed_data: Dict, output_filename: str) -> Dict:
        output_path = f"{self.base_path}/processed/{output_filename}"
        logging.info(f"Saving processed data to: {output_path}")

        async with aiofiles.open(output_path, 'w') as f:
            await f.write(json.dumps(processed_data, indent=2))

        output_size = os.path.getsize(output_path)
        logging.info(f"Processed data saved: {output_path} (Size: {output_size} bytes, Records: {processed_data['processed_count']})")

        return {
            "success": True,
            "output_path": output_path,
            "output_size": output_size,
            "records_saved": processed_data["processed_count"]
        }

    @activity.defn
    async def upload_to_external_service(self, file_path: str, service_url: str) -> Dict:
        logging.info(f"Uploading file {file_path} to {service_url}")
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                file_data = await f.read()

                data = aiohttp.FormData()
                data.add_field('file', file_data, filename=os.path.basename(file_path))

                async with session.post(service_url, data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        logging.info(f"Upload successful: {result.get('upload_id')}")
                        return {
                            "success": True,
                            "upload_id": result.get("upload_id"),
                            "service_response": result,
                            "uploaded_at": datetime.now().isoformat()
                        }
                    else:
                        logging.error(f"Upload failed with status: {response.status}")
                        raise Exception(f"Upload failed: {response.status}")

    @activity.defn
    async def send_notification(self, message: str, webhook_url: str) -> Dict:
        logging.info(f"Sending notification to {webhook_url}: {message}")
        async with aiohttp.ClientSession() as session:
            payload = {
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            }

            async with session.post(webhook_url, json=payload) as response:
                if response.status == 200:
                    logging.info(f"Notification sent successfully")
                    return {
                        "success": True,
                        "notification_sent": True,
                        "response_status": response.status
                    }
                else:
                    logging.error(f"Notification failed with status: {response.status}")
                    raise Exception(f"Notification failed: {response.status}")

    @activity.defn
    async def cleanup_temp_files(self, file_paths: List[str]) -> Dict:
        cleaned_files = []
        failed_files = []

        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    cleaned_files.append(file_path)
            except Exception as e:
                failed_files.append({"file": file_path, "error": str(e)})

        return {
            "success": True,
            "cleaned_files": cleaned_files,
            "failed_files": failed_files,
            "total_cleaned": len(cleaned_files)
        }

    @activity.defn
    async def log_processing_event(self, event_data: Dict) -> Dict:
        log_file = f"{self.base_path}/logs/processing_{datetime.now().strftime('%Y%m%d')}.log"

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_data.get("event_type", "unknown"),
            "data": event_data
        }

        async with aiofiles.open(log_file, 'a') as f:
            await f.write(json.dumps(log_entry) + '\n')

        return {
            "success": True,
            "log_file": log_file,
            "logged_at": datetime.now().isoformat()
        }

    @activity.defn
    async def rollback_upload(self, upload_id: str, service_url: str) -> Dict:
        logging.info(f"Rolling back upload {upload_id} from {service_url}")
        async with aiohttp.ClientSession() as session:
            rollback_url = f"{service_url}/rollback/{upload_id}"

            async with session.delete(rollback_url) as response:
                if response.status == 200:
                    logging.info(f"Rollback successful for upload {upload_id}")
                    return {
                        "success": True,
                        "rollback_id": upload_id,
                        "rollback_status": "completed"
                    }
                else:
                    logging.error(f"Rollback failed with status: {response.status}")
                    raise Exception(f"Rollback failed: {response.status}")

    @activity.defn
    async def restore_from_backup(self, backup_path: str, original_path: str) -> Dict:
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, original_path)
            return {
                "success": True,
                "restored_from": backup_path,
                "restored_to": original_path,
                "restored_at": datetime.now().isoformat()
            }
        else:
            raise Exception("Backup file not found")

    @activity.defn
    async def validate_processing_result(self, processed_data: Dict) -> Dict:
        if not processed_data.get("success"):
            raise Exception("Processing was not successful")

        if processed_data.get("processed_count", 0) == 0:
            raise Exception("No records were processed")

        return {
            "success": True,
            "validation_passed": True,
            "records_validated": processed_data.get("processed_count", 0),
            "validation_timestamp": datetime.now().isoformat()
        }
