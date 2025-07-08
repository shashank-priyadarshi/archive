#!/usr/bin/env python3
import asyncio
import subprocess
import sys
import time
import signal
import os
from pathlib import Path

class TemporalFileProcessingDemo:
    def __init__(self):
        self.processes = []
        self.base_dir = Path(__file__).parent

    def start_temporal_server(self):
        print("Starting Temporal server...")
        cmd = ["docker", "run", "--rm", "-p", "7233:7233", "temporalio/auto-setup:1.22.0"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes.append(("Temporal Server", process))
        print("Temporal server started")

    def start_sample_server(self):
        print("Starting sample server...")
        cmd = [sys.executable, str(self.base_dir / "sample_server.py")]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes.append(("Sample Server", process))
        print("Sample server started at http://localhost:8080")

    def start_worker(self):
        print("Starting Temporal worker...")
        cmd = [sys.executable, str(self.base_dir / "worker.py")]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes.append(("Worker", process))
        print("Worker started")

    def run_client(self):
        print("Running client...")
        cmd = [sys.executable, str(self.base_dir / "client.py")]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.processes.append(("Client", process))

        stdout, stderr = process.communicate()
        if stdout:
            print("Client output:")
            print(stdout.decode())
        if stderr:
            print("Client errors:")
            print(stderr.decode())

    def wait_for_services(self):
        print("Waiting for services to be ready...")
        time.sleep(5)

    def cleanup(self):
        print("\nShutting down all processes...")
        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"{name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"{name} force killed")
            except Exception as e:
                print(f"Error stopping {name}: {e}")

    def signal_handler(self, signum, frame):
        print(f"\nReceived signal {signum}, shutting down...")
        self.cleanup()
        sys.exit(0)

    def run(self):
        try:
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)

            print("Starting Temporal File Processing Demo...")
            print("=" * 50)

            self.start_temporal_server()
            time.sleep(3)

            self.start_sample_server()
            time.sleep(2)

            self.start_worker()
            time.sleep(3)

            self.wait_for_services()

            print("\nAll services started. Running client...")
            print("=" * 50)

            self.run_client()

        except KeyboardInterrupt:
            print("\nInterrupted by user")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cleanup()

if __name__ == "__main__":
    demo = TemporalFileProcessingDemo()
    demo.run()
