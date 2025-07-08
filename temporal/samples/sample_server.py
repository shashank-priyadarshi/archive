import asyncio
import json
import os
import uuid
from datetime import datetime
from aiohttp import web, FormData
from aiohttp.web import Request, Response
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SampleServer:
    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.uploads = {}
        self.setup_routes()

        self.base_path = os.path.join(os.getcwd(), "temporal_samples_data")
        self.ensure_directories()

    def ensure_directories(self):
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(f"{self.base_path}/uploads", exist_ok=True)
        os.makedirs(f"{self.base_path}/logs", exist_ok=True)
        logger.info(f"Sample server data directory: {self.base_path}")

    def setup_routes(self):
        self.app.router.add_post('/upload', self.handle_upload)
        self.app.router.add_delete('/rollback/{upload_id}', self.handle_rollback)
        self.app.router.add_post('/webhook', self.handle_webhook)
        self.app.router.add_get('/health', self.handle_health)
        self.app.router.add_get('/sample-data/posts', self.sample_posts)
        self.app.router.add_get('/sample-data/users', self.sample_users)
        self.app.router.add_get('/sample-data/albums', self.sample_albums)

    async def handle_upload(self, request: Request) -> Response:
        try:
            data = await request.post()
            file_field = data.get('file')

            if not file_field:
                return web.json_response(
                    {"error": "No file provided"},
                    status=400
                )

            upload_id = str(uuid.uuid4())
            filename = file_field.filename or f"upload_{upload_id}"
            file_path = os.path.join(self.base_path, "uploads", filename)

            with open(file_path, 'wb') as f:
                f.write(file_field.file.read())

            file_size = os.path.getsize(file_path)

            self.uploads[upload_id] = {
                "filename": filename,
                "file_path": file_path,
                "uploaded_at": datetime.now().isoformat(),
                "file_size": file_size
            }

            logger.info(f"File uploaded: {filename} (ID: {upload_id}, Size: {file_size} bytes)")

            return web.json_response({
                "upload_id": upload_id,
                "filename": filename,
                "file_size": file_size,
                "uploaded_at": datetime.now().isoformat(),
                "status": "success"
            })

        except Exception as e:
            logger.error(f"Upload error: {e}")
            return web.json_response(
                {"error": str(e)},
                status=500
            )

    async def handle_rollback(self, request: Request) -> Response:
        try:
            upload_id = request.match_info['upload_id']

            if upload_id not in self.uploads:
                return web.json_response(
                    {"error": "Upload not found"},
                    status=404
                )

            upload_info = self.uploads[upload_id]
            file_path = upload_info["file_path"]

            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File rolled back: {upload_info['filename']} (ID: {upload_id})")

            del self.uploads[upload_id]

            return web.json_response({
                "rollback_id": upload_id,
                "status": "completed",
                "rolled_back_at": datetime.now().isoformat()
            })

        except Exception as e:
            logger.error(f"Rollback error: {e}")
            return web.json_response(
                {"error": str(e)},
                status=500
            )

    async def handle_webhook(self, request: Request) -> Response:
        try:
            payload = await request.json()

            webhook_log = {
                "received_at": datetime.now().isoformat(),
                "payload": payload,
                "headers": dict(request.headers)
            }

            log_file = os.path.join(self.base_path, "logs", f"webhook_{datetime.now().strftime('%Y%m%d')}.log")
            with open(log_file, 'a') as f:
                f.write(json.dumps(webhook_log) + '\n')

            logger.info(f"Webhook received: {payload.get('message', 'No message')}")

            return web.json_response({
                "status": "received",
                "timestamp": datetime.now().isoformat()
            })

        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return web.json_response(
                {"error": str(e)},
                status=500
            )

    async def handle_health(self, request: Request) -> Response:
        return web.json_response({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uploads_count": len(self.uploads)
        })

    async def sample_posts(self, request: Request) -> Response:
        sample_data = [
            {
                "id": 1,
                "title": "Sample Post 1",
                "body": "This is the body of sample post 1",
                "userId": 1
            },
            {
                "id": 2,
                "title": "Sample Post 2",
                "body": "This is the body of sample post 2",
                "userId": 1
            },
            {
                "id": 3,
                "title": "Sample Post 3",
                "body": "This is the body of sample post 3",
                "userId": 2
            }
        ]

        logger.info(f"Serving sample posts data: {len(sample_data)} posts")
        return web.json_response(sample_data)

    async def sample_users(self, request: Request) -> Response:
        sample_data = [
            {
                "id": 1,
                "name": "John Doe",
                "username": "johndoe",
                "email": "john@example.com",
                "phone": "123-456-7890"
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "username": "janesmith",
                "email": "jane@example.com",
                "phone": "098-765-4321"
            },
            {
                "id": 3,
                "name": "Bob Johnson",
                "username": "bobjohnson",
                "email": "bob@example.com",
                "phone": "555-123-4567"
            }
        ]

        logger.info(f"Serving sample users data: {len(sample_data)} users")
        return web.json_response(sample_data)

    async def sample_albums(self, request: Request) -> Response:
        sample_data = [
            {
                "id": 1,
                "title": "Sample Album 1",
                "userId": 1
            },
            {
                "id": 2,
                "title": "Sample Album 2",
                "userId": 1
            },
            {
                "id": 3,
                "title": "Sample Album 3",
                "userId": 2
            },
            {
                "id": 4,
                "title": "Sample Album 4",
                "userId": 3
            }
        ]

        logger.info(f"Serving sample albums data: {len(sample_data)} albums")
        return web.json_response(sample_data)

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()

        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

        logger.info(f"Sample server started at http://{self.host}:{self.port}")
        logger.info(f"Available endpoints:")
        logger.info(f"  POST /upload - File upload endpoint")
        logger.info(f"  DELETE /rollback/{{upload_id}} - Rollback upload")
        logger.info(f"  POST /webhook - Notification webhook")
        logger.info(f"  GET /health - Health check")
        logger.info(f"  GET /sample-data/posts - Sample posts data")
        logger.info(f"  GET /sample-data/users - Sample users data")
        logger.info(f"  GET /sample-data/albums - Sample albums data")

        return runner

    async def stop(self, runner):
        await runner.cleanup()
        logger.info("Sample server stopped")

async def main():
    server = SampleServer()
    runner = await server.start()

    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    finally:
        await server.stop(runner)

if __name__ == "__main__":
    asyncio.run(main())
