# Mastering Temporal CLI Batch Operations for Distributed Systems Management

## 1. Introduction to Temporal Batch Operations

In the realm of distributed systems, managing a multitude of long-running processes is a common yet complex challenge. Temporal, as a robust orchestration engine, provides powerful mechanisms to define and execute durable workflows. Beyond individual workflow management, there often arises a critical need to interact with or modify a large number of these workflows simultaneously. This is where Temporal's batch operations become indispensable.

Batch operations in Temporal refer to the capability to initiate a single command that systematically affects multiple Workflow Executions. These operations are designed to run asynchronously in the background, processing each targeted Workflow Execution one at a time. This sequential, yet automated, approach ensures the durability and reliability of the operations, even when dealing with thousands or millions of workflows. The underlying Temporal platform guarantees that these bulk actions are completed resiliently, even in the face of system failures or restarts.

The importance of such capabilities in complex distributed environments cannot be overstated. Scenarios frequently emerge where system administrators or developers must perform bulk administrative tasks, react to system-wide events, or apply broad changes across their application landscape. Examples include:

- Updating a feature flag for all active customer order workflows
- Terminating obsolete long-running data processing jobs
- Initiating a mass reset of workflows after a critical bug fix has been deployed

Without dedicated batch capabilities, these tasks would necessitate tedious, error-prone, and often manual interventions, making large-scale system management impractical and risky. Temporal's batch operations streamline these processes, offering a controlled and auditable way to manage distributed application state at scale.

## 2. Understanding Temporal CLI and tctl Deprecation

The command-line interface (CLI) serves as a primary tool for developers and operators to interact with a Temporal Cluster. Historically, `tctl` was the foundational CLI tool for these interactions, enabling users to perform various operations on namespaces, workflows, task queues, and more. However, the Temporal project has evolved its tooling, and `tctl` has since been deprecated. It is no longer actively supported, and the official recommendation is for users to transition to the newer `temporal` CLI for all cluster interactions.

This transition is crucial for:
- Accessing new features
- Benefiting from ongoing support
- Aligning with the future direction of the Temporal ecosystem

Despite the deprecation, `tctl-v1` retains the ability to execute batch and batch-v2 commands. This backward compatibility layer is a deliberate design choice to facilitate a smoother migration path for existing users and their operational scripts. It acknowledges the practical challenges of a hard cut-over in production environments, allowing organizations to gradually transition their automation and procedures to the `temporal` CLI without immediate disruption.

**Important**: For all new development, automation, and long-term operational strategies, exclusive adoption of the `temporal` CLI is strongly advised.

The shift from `tctl` to the `temporal` CLI represents more than a mere renaming of a tool; it signifies a strategic evolution in Temporal's operational interface. The continued, albeit limited, support for `tctl-v1`'s batch commands underscores Temporal's commitment to operational continuity for its user base during this transition.

## 3. Core Batch Management Commands (`temporal batch`)

The `temporal batch` command set is specifically designed for managing the lifecycle and status of batch jobs themselves, which are long-running operations executed by the Temporal Service. These commands provide visibility into, and control over, the batch processes that are affecting multiple workflow executions.

### `temporal batch describe` - Monitoring Batch Job Progress

The `temporal batch describe` command is used to retrieve and display detailed information about an ongoing or completed batch job. This functionality is essential for operators to monitor the progress of large-scale operations, understand their current status, and diagnose any issues that may arise during execution.

**Usage:**
```bash
temporal batch describe --job-id <YourJobId> [--namespace <YourNamespace>]
```

**Parameters:**
- `--job-id <string>`: This is a mandatory parameter that specifies the unique identifier of the batch job whose details are to be displayed.
- `--namespace, -n <string>`: This optional parameter specifies the Temporal Service Namespace where the batch job is located. If omitted, the command defaults to the "default" namespace.

**Example:**
```bash
temporal batch describe --job-id my-batch-reset-job-123 --namespace production
```

This command would return information such as the job's status (e.g., running, completed, failed), the number of workflows processed, and any associated error messages.

### `temporal batch list` - Listing Active and Completed Batch Jobs

The `temporal batch list` command provides an overview of batch jobs, allowing operators to retrieve a list of active or completed batch operations within a specified namespace or across the entire Temporal Service.

**Usage:**
```bash
temporal batch list [--namespace <YourNamespace>] [--limit <int>]
```

**Parameters:**
- `--namespace, -n <string>`: This optional parameter specifies the Temporal Service Namespace from which to list batch jobs. It defaults to the "default" namespace if not provided.
- `--limit <int>`: This optional parameter specifies the maximum number of batch jobs to display in the output. This is useful for managing the volume of information returned, especially in environments with many batch operations.

**Example:**
```bash
temporal batch list --limit 100
```

This command provides a concise summary of each batch job, including its ID, type, status, and creation time, enabling quick assessment of the system's batch processing activity.

### `temporal batch terminate` - Halting Ongoing Batch Operations

The `temporal batch terminate` command is used to stop an active batch job. This action is typically taken when a batch operation is no longer necessary, has been misconfigured, or is causing unintended side effects that require immediate cessation.

**Usage:**
```bash
temporal batch terminate --job-id <YourJobId> --reason <YourTerminationReason>
```

**Parameters:**
- `--job-id <string>`: This is a mandatory parameter specifying the unique identifier of the batch job to be terminated.
- `--reason <string>`: This is a mandatory parameter requiring a descriptive explanation for terminating the batch job. This reason is recorded in the system logs and is crucial for auditing and post-mortem analysis.

**Example:**
```bash
temporal batch terminate --job-id my-signal-campaign-456 --reason "Incorrect query, stopping signal campaign"
```

### Irreversibility and Operational Caution

A critical aspect of `temporal batch terminate` is its operational characteristic: **terminating a batch job does not roll back any operations that have already been performed by that job**. This means that if a batch operation has already processed a certain number of workflows before termination, those workflows remain in their modified state. The termination command merely stops any further processing by the batch job.

This behavior highlights a significant design principle within Temporal's batch processing: operations are durable and committed as they occur. There is no inherent "undo" mechanism for batch operations. This necessitates a high degree of caution and meticulous planning before initiating any large-scale batch operation, particularly those with potentially destructive or irreversible effects, such as mass terminations or resets.

## 4. Batch Operations on Workflows via CLI

The modern `temporal` CLI handles batch operations that directly affect Workflow Executions primarily through specialized `temporal workflow` commands, leveraging the powerful `--query` flag for targeting. This approach differs from the `tctl` paradigm, which often used a `batch start` command with a `--batch_type` flag.

### `temporal workflow signal --query` - Signaling Multiple Workflows

The `temporal workflow signal --query` command enables the sending of a signal to a collection of Workflow Executions that are identified by a visibility query. This is a fundamental pattern in Temporal for notifying multiple running workflows about an external event, a change in system state, or to trigger specific logic within them without directly interacting with each workflow individually.

**Usage:**
```bash
temporal workflow signal --query "<SQL-like query>" --name "<SignalName>" --input '<JSON_Input>' --reason "<Reason>" [--namespace <YourNamespace>]
```

**Parameters:**
- `--query "<SQL-like query>"`: This is a mandatory parameter that specifies an SQL-like query of Search Attributes. This query filters and identifies the specific Workflow Executions that will receive the signal.
- `--name "<SignalName>"`: This mandatory parameter defines the name of the signal method that is expected to be invoked within the target workflows.
- `--input '<JSON_Input>'`: This optional parameter provides the input payload for the signal, which must be in JSON format. This allows for passing specific data along with the signal to the workflows.
- `--reason "<Reason>"`: This optional parameter allows for a descriptive reason to be provided for sending the signal. This reason is recorded in the workflow's history, aiding in auditing and debugging.
- `--namespace, -n <string>`: This optional parameter specifies the target namespace for the operation.

**Example:**
```bash
temporal workflow signal --query "WorkflowType='OrderProcessingWorkflow' AND ExecutionStatus='Running'" \
    --name "cancelOrder" \
    --input '{"reason": "Product recall"}' \
    --reason "Mass cancellation due to product recall"
```

### `temporal workflow reset-batch` - Resetting Batches of Workflow Executions

The `temporal workflow reset-batch` command is a powerful administrative tool used to revert the state of multiple Workflow Executions simultaneously to a previous point in their history. This capability is invaluable for disaster recovery, applying code fixes to running workflows that encountered a bug, or correcting data inconsistencies across a large set of workflow instances.

**Usage:**
```bash
temporal workflow reset-batch --query "<SQL-like query>" --reason "<Reason>" --type <ResetType> [--dry-run] \
    [--input_file <filename>] [--exclude_file <filename>] [--only_non_deterministic] [--reset_bad_binary_checksum <checksum>]
```

**Parameters:**
- `--query "<SQL-like query>"`: This is a mandatory parameter that uses an SQL-like query of Search Attributes to identify the specific Workflow Executions that are targeted for the reset operation.
- `--reason "<Reason>"`: This is a mandatory parameter requiring a descriptive reason for performing the batch reset. This reason is crucial for auditing and is recorded in the Event History of each affected workflow.
- `--type <ResetType>`: This mandatory parameter specifies the exact point in the Workflow's Event History to which it will be reverted:
  - `FirstWorkflowTask`: Resets the workflow's state to the very beginning of its Event History.
  - `LastWorkflowTask`: Resets the workflow's state to the last successfully executed Workflow task.
  - `LastContinuedAsNew`: Resets the workflow's state to the last point where the workflow was "continued as new."
  - `WorkflowExecutionSignaled`: Resets to the point where a WorkflowExecutionSignaled event occurred.
- `--dry-run`: This optional but highly recommended flag simulates the batch reset operation without actually modifying any workflow states.
- `--input_file <filename>`: Provides an input file containing a list of Workflow IDs to reset.
- `--exclude_file <filename>`: Provides an input file containing Workflow IDs to exclude from the reset operation.
- `--only_non_deterministic`: If specified, the workflow execution will be reset only if its last event was a WorkflowTaskFailed with a non-determinism error.
- `--reset_bad_binary_checksum <checksum>`: This parameter is used in conjunction with a BadBinary reset type to specify the binary checksum of the problematic worker code.

**Example:**
```bash
# Dry run first
temporal workflow reset-batch --query "WorkflowType='LoyaltyProgram'" \
    --reason "Applying fix for loyalty calculation bug" \
    --type LastWorkflowTask \
    --dry-run

# After verifying the dry run output, execute the actual reset
temporal workflow reset-batch --query "WorkflowType='LoyaltyProgram'" \
    --reason "Applying fix for loyalty calculation bug" \
    --type LastWorkflowTask
```

### `temporal workflow list --query` - Querying Multiple Workflows in a Batch Context

While `temporal workflow query` is typically used to retrieve the state of a single workflow execution, the `temporal workflow list --query` command is the primary and most effective tool for identifying and filtering multiple Workflow Executions based on their Search Attributes.

**Usage:**
```bash
temporal workflow list --query "<SQL-like query>" [--limit <int>] [--open]
```

**Parameters:**
- `--query "<SQL-like query>"`: This is a mandatory parameter that accepts an SQL-like query string to filter workflow executions based on their Search Attributes.
- `--status <Status>`: This optional parameter allows filtering by the workflow execution status, such as Running, Completed, or Failed.
- `--limit <int>`: This optional parameter specifies the maximum number of workflow executions to list in the output.
- `--open`: This optional flag, when present, restricts the listing to only open (currently running) workflow executions.

**Example:**
```bash
# List all running workflows of type DataProcessingWorkflow started within the last 24 hours
temporal workflow list --query "WorkflowType='DataProcessingWorkflow' AND StartTime > '24h'" --status Running

# List all completed workflows with a specific custom search attribute
temporal workflow list --query "CustomID = 'XYZ789'" --status Completed
```

### Visibility as the Foundation for Batch Operations

The extensive reliance on the `--query` flag across `temporal workflow signal`, `temporal workflow reset-batch`, and `temporal workflow list` commands underscores a fundamental architectural dependency within Temporal's operational capabilities. The accuracy and efficiency of these batch operations are directly tied to the underlying visibility store and its Search Attributes.

**Important Considerations:**

1. **Advanced Visibility Required**: The `--query` flag is only supported when Advanced Visibility is configured. This implies that for organizations to fully leverage the robust, large-scale batch management features of Temporal, a basic Temporal setup might not suffice.

2. **Eventual Consistency**: The visibility store operates with eventual consistency. This means that while powerful, queries against this store might not reflect real-time state changes instantaneously. There can be a slight delay between a workflow's actual state transition and its propagation and indexing within the visibility store.

## 5. Common Flags and Global Options

Temporal CLI commands, including those used for batch operations, support a variety of global flags. These flags allow for consistent configuration of connection details, logging behavior, and other operational parameters across different commands.

| Flag Name | Alias | Description | Default Value | Environment Variable |
|-----------|-------|-------------|---------------|---------------------|
| `--address` | | Temporal Service gRPC endpoint. | `127.0.0.1:7233` | `TEMPORAL_CLI_ADDRESS` |
| `--api-key` | | API key for requests. | `None` | |
| `--codec-auth` | | Authorization header for Codec Server requests. | `None` | |
| `--codec-endpoint` | | Remote Codec Server endpoint. | `None` | |
| `--codec-header` | | HTTP headers for requests to codec server (KEY=VALUE). | `None` | |
| `--color` | | Output coloring. Accepted values: always, never, auto. | `auto` | |
| `--command-timeout` | | The command execution timeout. 0s means no timeout. | `0s` | |
| `--env` | | Active environment name (ENV). | `default` | |
| `--env-file` | | Path to environment settings file. | `$HOME/.config/temporalio/temporal.yaml` | |
| `--grpc-meta` | | HTTP headers for requests (KEY=VALUE). | `None` | |
| `--log-format` | | Log format. Accepted values: text, json. | `text` | |
| `--log-level` | | Log level. Accepted values: debug, info, warn, error, never. | `info` | |
| `--namespace` | `-n` | Temporal Service Namespace. | `default` | `TEMPORAL_CLI_NAMESPACE` |
| `--no-json-shorthand-payloads` | | Raw payload output, even if the JSON option was used. | `false` | |
| `--tls_ca_path` | | Path to a server Certificate Authority (CA) certificate file. | `None` | `TEMPORAL_CLI_TLS_CA` |
| `--tls_cert_path` | | Path to a public X.509 certificate file for mutual TLS authentication. | `None` | `TEMPORAL_CLI_TLS_CERT` |
| `--tls_disable_host_verification` | | Disable verification of the server certificate. | `false` | `TEMPORAL_CLI_TLS_DISABLE_HOST_VERIFICATION` |
| `--tls_key_path` | | Path to a private key file for mutual TLS authentication. | `None` | `TEMPORAL_CLI_TLS_KEY` |
| `--tls_server_name` | | Override target TLS server name used for TLS host verification. | `None` | |

The ability to set these global flags via environment variables is a significant advantage for operational efficiency. This practice enables the creation of cleaner, more portable scripts, as sensitive or frequently used parameters do not need to be explicitly included in every command line invocation.

## 6. Best Practices for Batch Operations

Effective and safe utilization of Temporal CLI batch operations requires adherence to several best practices:

### 1. Prioritize `temporal` CLI
Always use the modern `temporal` CLI over the deprecated `tctl` for new development and automation. This ensures access to the latest features, bug fixes, and long-term support.

### 2. Leverage `--dry-run` for reset-batch
The `--dry-run` flag for `temporal workflow reset-batch` is an indispensable safety mechanism. Always perform a dry run before executing any actual batch reset to verify that the query correctly identifies the target workflows and to understand the scope of the operation.

### 3. Understand Eventual Consistency
Be aware that the visibility store, which powers the `--query` functionality, is eventually consistent. This implies that real-time state changes might not be immediately reflected in query results. For critical operations, consider potential delays in visibility data propagation.

### 4. Use Descriptive `--reason` Flags
For all batch operations that support it (e.g., signal, reset-batch, terminate), provide clear and descriptive reasons. These reasons are permanently recorded in the workflow's event history and are invaluable for auditing, debugging, and understanding the context of past administrative actions.

### 5. Acknowledge Irreversibility of Termination
Remember that `temporal batch terminate` stops future processing but does not roll back already completed operations. This characteristic means that any actions performed by the batch job before its termination are permanent.

### 6. Utilize Global Flags and Environment Variables
For consistent and streamlined operations, leverage global CLI flags and their corresponding environment variables. This practice simplifies scripting, reduces command-line clutter, and ensures that operations are consistently targeting the correct cluster and namespace.

### 7. Monitor Batch Job Progress
Regularly use `temporal batch describe` to monitor the progress of ongoing batch jobs. This proactive monitoring allows for early detection of issues and provides the necessary information to decide whether to continue or terminate a job.

## 7. Conclusion

Temporal CLI batch operations provide powerful capabilities for managing and interacting with large numbers of workflow executions in a distributed system. The transition from the deprecated `tctl` to the modern `temporal` CLI marks a significant evolution in Temporal's operational tooling, offering a more streamlined and future-proof interface.

While core batch management commands like `describe`, `list`, and `terminate` provide control over the batch jobs themselves, operations directly affecting workflows, such as signaling and resetting, are now integrated with the `temporal workflow` command family, primarily leveraging the robust `--query` mechanism.

A profound understanding of the underlying visibility store, its eventual consistency, and the critical role of Advanced Visibility configuration is paramount for effective batch targeting. Furthermore, the irreversible nature of certain operations, like batch termination, and the indispensable safety net provided by features like dry-run for batch resets, underscore the necessity of meticulous planning and cautious execution.

By adhering to established best practices, including thorough testing, descriptive logging, and consistent configuration through global flags and environment variables, operators can harness the full potential of Temporal's batch capabilities to manage complex distributed applications with efficiency, reliability, and confidence.

---

# Building Resilient Applications: A Deep Dive into Standalone Temporal Python Workers

## 1. Introduction to Temporal Python Workers

In the architecture of a Temporal application, workers serve as the critical bridge between your application code and the Temporal Cluster. They are the execution hosts responsible for polling the Temporal Service for tasks, executing the business logic defined in your workflows and activities, and returning the results back to the cluster. Without workers, the Temporal Cluster, while orchestrating the durable execution, would have no means to actually run your custom application code.

The Temporal Python SDK provides a comprehensive framework for authoring these workflows and activities using the Python programming language. It abstracts away much of the complexity inherent in distributed systems, allowing developers to focus on defining their business logic as durable, fault-tolerant workflows.

Python workers continuously long-poll the Temporal Service for new workflow tasks and activity tasks assigned to their specific task queues. Upon receiving a task, the worker executes the corresponding workflow or activity function and then reports the outcome back to the Temporal Cluster. This polling mechanism and the worker's role in executing code are fundamental to Temporal's ability to ensure that application logic durably executes even in the face of worker failures, network partitions, or other infrastructure issues.

## 2. Setting Up Your Python Development Environment

Before diving into the specifics of defining and running Temporal Python workers, it is essential to establish a suitable development environment. The Temporal Python SDK requires Python version 3.9 or newer to function correctly.

### Environment Setup

A recommended approach for setting up the environment and managing dependencies involves using tools like `uv`. After ensuring Python 3.9+ is installed (e.g., `uv python install 3.13`), developers can clone the Temporal Python samples repository and install all required dependencies by running `uv sync` from the project root.

### Project Structure

For organizing a Temporal application project, a best practice involves structuring the codebase logically. A common and highly recommended project layout includes separate directories for activities, workflows, client code (for starting workflows), and workers.

**Example project structure:**
```bash
mkdir -p data-processing-service/{activities,workflows,client,workers/python}
```

This separation of concerns enhances code readability, maintainability, and allows for independent scaling and deployment of different components.

## 3. Connecting to the Temporal Server

A standalone Temporal Python worker must establish a connection to a Temporal Cluster to poll for tasks and report results. This connection is managed through a `Client` instance provided by the Temporal Python SDK.

### Client Initialization and Connection Options

The `Client.connect()` method is the primary interface for establishing a connection to the Temporal server. This method typically takes the server's gRPC address as its first argument, such as `"localhost:7233"` for a local development setup. An optional `namespace` argument can also be provided to specify the target Temporal Namespace for operations.

**Important Note**: A `Client` instance in the Python SDK does not have an explicit `close()` method; its lifecycle is typically managed implicitly or through the worker's shutdown.

### Connection Methods

Temporal offers flexibility in how a client connects to its cluster, adapting to various deployment environments:

#### Local Development Server
For rapid local development and initial testing, a Temporal development server can be started using:

```bash
temporal server start-dev --db-filename temporal.db --ui-port 8080
```

This command automatically sets up a local database, starts the Temporal Web UI (typically at `http://localhost:8080` or `http://localhost:8233`), and creates a default Namespace. Workers connect to this local server using `localhost:7233`.

#### Temporal Cloud
For production use cases or scalable proofs of concept, Temporal Cloud is the recommended environment. Connecting to Temporal Cloud requires specific credentials:

- Temporal Cloud Namespace ID
- Namespace's gRPC endpoint (format: `namespace.unique_id.tmprl.cloud:port`)
- SSL certificate (.pem) and private key (.key) files for mTLS authentication

**Example connection:**
```python
client = await Client.connect(
    "your-namespace.unique-id.tmprl.cloud:7233",
    namespace="your-namespace",
    tls=True,
    tls_cert="path/to/cert.pem",
    tls_key="path/to/key.pem"
)
```

#### Self-hosted Temporal Cluster
For scenarios requiring production-level features with customizability, deploying a self-hosted Temporal Cluster via Docker is an option:

```bash
# Clone and start the cluster
git clone https://github.com/temporalio/docker-compose.git
cd docker-compose
docker compose up
```

Workers need to be configured with the appropriate IP address and port to connect to the Temporal Server container within the Docker network.

## 4. Defining Temporal Workflows in Python

In the Temporal Python SDK, a workflow is defined as a Python class. This class encapsulates the durable, fault-tolerant business logic that orchestrates activities and manages long-running processes.

### Workflow Class Structure

A workflow class is identified by the `@workflow.defn` decorator. This decorator can optionally take a `name` parameter to customize the workflow's registered name, or `dynamic=True` to designate it as a catch-all for otherwise unhandled workflow types.

The core execution logic of a workflow resides in a single method decorated with `@workflow.run`. This method must be an `async def` function, signifying its asynchronous nature. The first parameter of this method must be `self`, followed by any positional arguments that represent the inputs to the workflow.

**Example workflow:**
```python
# workflows.py
from temporalio import workflow
from datetime import timedelta

# Import activity from a separate file
with workflow.unsafe.imports_passed_through():
    from .activities import process_data_activity

@workflow.defn
class DataProcessingWorkflow:
    @workflow.init
    def __init__(self, initial_data: str):
        self.current_data = initial_data
        workflow.logger.info(f"Workflow initialized with: {self.current_data}")

    @workflow.run
    async def run(self, input_data: str) -> str:
        workflow.logger.info(f"Starting DataProcessingWorkflow with input: {input_data}")

        # Execute an activity
        processed_result = await workflow.execute_activity(
            process_data_activity,
            input_data,
            schedule_to_close_timeout=timedelta(seconds=30),
        )

        self.current_data = processed_result
        workflow.logger.info(f"Workflow completed. Final data: {self.current_data}")
        return processed_result

    @workflow.signal
    async def update_data(self, new_data: str):
        self.current_data = new_data
        workflow.logger.info(f"Data updated via signal: {self.current_data}")

    @workflow.query
    def get_current_data(self) -> str:
        return self.current_data

    @workflow.update
    async def append_to_data(self, suffix: str) -> str:
        # Validator for the update
        @append_to_data.validator
        def validate(self, suffix: str):
            if not suffix:
                raise ValueError("Suffix cannot be empty")

        self.current_data += suffix
        workflow.logger.info(f"Data appended via update: {self.current_data}")
        return self.current_data
```

### Deterministic Constraints and the Workflow Sandbox

A cornerstone of Temporal's durability and fault tolerance is the strict requirement that workflow code must be deterministic. This means that given the same history of events, a workflow execution must always produce the same sequence of commands.

**Workflow code must avoid:**
- Non-deterministic functions (random number generators, UUID.randomUUID(), etc.)
- Direct I/O or Service Calls (network I/O, database calls, external services)
- Mutable Global Variables
- Native Threading or Blocking Concurrency
- System Time (use `workflow.now()` instead of `datetime.now()`)

The Temporal Python SDK runs workflow code within a specialized sandbox environment by default. This sandbox restricts access to certain non-deterministic operations, raising errors if violations occur.

### Signal, Query, and Update Handlers

Temporal workflows can interact with external systems and receive external input through signals, queries, and updates:

#### Signals (`@workflow.signal`)
A signal method is used to send asynchronous messages to a running workflow. It can be an `async` or non-`async` method. Signal methods can mutate workflow state and initiate other workflow operations.

#### Queries (`@workflow.query`)
A query method is used to synchronously retrieve the current state of a workflow. It should return a value but must not be an `async` method, nor should it mutate any workflow state.

#### Updates (`@workflow.update`)
Updates are a more recent and robust mechanism for interacting with workflows, offering both input and a return value. They can be `async` or non-`async` and are allowed to mutate workflow state and make calls to other workflow APIs.

## 5. Defining Temporal Activities in Python

Activities in Temporal represent the actual side effects that interact with the outside world. Unlike workflows, activities are not constrained by determinism and can perform any operation, such as database calls, API requests, or complex computations.

### Activity Function Structure

An activity is defined as a Python function decorated with `@activity.defn`. Similar to workflows, a custom name for the activity can be set with a decorator argument, or `dynamic=True` can be used for a catch-all activity.

**Example activities:**
```python
# activities.py
from temporalio import activity
import time
import random
import asyncio

@activity.defn
def process_data_activity(data: str) -> str:
    """
    A synchronous activity that simulates data processing.
    """
    activity.logger.info(f"Processing data: {data}")
    # Simulate a blocking I/O or CPU-intensive task
    time.sleep(random.uniform(1, 3))
    processed_data = data.upper() + "-PROCESSED"
    activity.logger.info(f"Finished processing. Result: {processed_data}")
    return processed_data

@activity.defn
async def fetch_external_resource(url: str) -> str:
    """
    An asynchronous activity that simulates fetching an external resource.
    """
    activity.logger.info(f"Fetching resource from: {url}")
    # Simulate an async network call
    await asyncio.sleep(1)
    return f"Content from {url}"

@activity.defn
def long_running_activity(task_id: str) -> str:
    """
    A long-running activity that heartbeats and handles cancellation.
    """
    for i in range(10):
        try:
            activity.logger.info(f"Long-running task {task_id}: step {i+1}/10")
            time.sleep(2)  # Simulate work
            activity.heartbeat(f"Progress: {i+1}/10")  # Report progress
        except activity.CancelledError:
            activity.logger.warning(f"Long-running task {task_id} cancelled at step {i+1}")
            raise  # Re-raise to propagate cancellation
    return f"Long-running task {task_id} completed."
```

### Synchronous vs. Asynchronous Activities

Activities can be defined as either synchronous (`def`) or asynchronous (`async def`) functions. Asynchronous activities are generally more performant, especially for I/O-bound tasks, as they allow the worker to handle multiple activities concurrently on a single thread while waiting for I/O operations to complete.

### Heartbeating and Cancellation

For long-running activities, it is crucial to implement heartbeating and handle cancellation:

- **Heartbeating** (`activity.heartbeat()`) informs the Temporal Cluster that the activity is still alive and making progress
- **Cancellation** should be handled gracefully by checking for `activity.CancelledError` and cleaning up resources

### Data Serialization and Converters

All parameters passed to and returned from activity functions must be serializable. The Temporal Python SDK's default data converter supports a wide range of types, including:

- `None`, `bytes`, `google.protobuf.message.Message`
- `dataclasses`, `iterables`, `Pydantic` models
- `IntEnum`/`StrEnum` based enumerates, `UUID`

**Note**: The default converter does not natively support `date`, `time`, or `datetime` objects. For complex or custom data types, developers can implement custom payload converters.

## 6. Registering Workflows and Activities with a Worker

Once workflows and activities are defined, they must be registered with a `Worker` instance. The Worker is the runtime component that polls for tasks, dispatches them to the appropriate workflow or activity function, and manages their execution lifecycle.

**Example worker setup:**
```python
# worker_main.py
import asyncio
import concurrent.futures
from temporalio.client import Client
from temporalio.worker import Worker
import logging

# Configure logging for visibility
logging.basicConfig(level=logging.INFO)

# Import your workflow and activities
from .workflows import DataProcessingWorkflow
from .activities import process_data_activity, fetch_external_resource, long_running_activity

async def run_worker():
    # 1. Initialize a Temporal Client
    client = await Client.connect("localhost:7233", namespace="default")

    # 2. Configure an activity executor for synchronous activities
    activity_executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)

    # 3. Create a new Worker instance
    worker = Worker(
        client,
        task_queue="my-data-processing-task-queue",
        workflows=[DataProcessingWorkflow],
        activities=[process_data_activity, fetch_external_resource, long_running_activity],
        activity_executor=activity_executor,  # Pass the executor for synchronous activities
        # Other optional worker parameters can be set here
        # max_concurrent_activities=50,
        # max_activities_per_second=100.0,
    )

    logging.info("Worker started, polling task queue 'my-data-processing-task-queue'...")

    # 4. Call run on the Worker to start polling and executing tasks
    try:
        async with worker:
            # Keep the worker running indefinitely until a shutdown signal is received
            await asyncio.Future()  # Awaiting a never-resolving future keeps the worker alive
    except asyncio.CancelledError:
        logging.info("Worker shutdown initiated.")
    finally:
        activity_executor.shutdown(wait=True)
        logging.info("Worker gracefully shut down.")

if __name__ == "__main__":
    asyncio.run(run_worker())
```

## 7. Managing the Worker Lifecycle

The lifecycle of a Temporal Python worker involves starting it to begin polling for tasks and gracefully shutting it down when it is no longer needed.

### Starting and Stopping Workers

A `Worker` instance can be run explicitly using the `worker.run()` method, which is an async function that will continuously poll for tasks until a shutdown is initiated. Alternatively, and often preferred in asynchronous Python applications, the worker can be managed using an async with statement.

**Example of controlled shutdown:**
```python
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from .workflows import MyWorkflow
from .activities import my_activity

async def run_worker_with_controlled_shutdown(stop_event: asyncio.Event):
    client = await Client.connect("localhost:7233", namespace="my-namespace")
    worker = Worker(client, task_queue="my-task-queue", workflows=[MyWorkflow], activities=[my_activity])

    try:
        async with worker:
            await stop_event.wait()  # Worker runs until stop_event is set
            logging.info("Stop event received, initiating worker shutdown.")
    except asyncio.CancelledError:
        logging.info("Worker task was cancelled.")
    finally:
        logging.info("Worker context exited.")

async def main():
    stop_event = asyncio.Event()

    # In a real application, you might set up signal handlers here
    # asyncio.get_event_loop().add_signal_handler(signal.SIGINT, stop_event.set)
    # asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, stop_event.set)

    worker_task = asyncio.create_task(run_worker_with_controlled_shutdown(stop_event))

    # Simulate some work or wait for a condition to stop the worker
    await asyncio.sleep(60)  # Run worker for 60 seconds
    stop_event.set()  # Signal the worker to stop

    await worker_task  # Wait for the worker to complete its shutdown
    logging.info("Application finished.")

if __name__ == "__main__":
    asyncio.run(main())
```

### Graceful Shutdown

For robust deployments, graceful shutdown is paramount. The `Worker` constructor includes a `graceful_shutdown_timeout` parameter, which accepts a `datetime.timedelta`. When this timeout is set, the worker will notify any running activities of an impending graceful shutdown before forcefully cancelling them.

## 8. Concurrency Configuration for Python Workers

Optimizing the concurrency settings of Temporal Python workers is crucial for achieving efficient resource utilization and high throughput.

### Activity Executors

The choice of executor for activities is a key consideration, especially for synchronous (blocking) activities:

#### Synchronous Multithreaded Activities
For synchronous activities (functions defined with `def` rather than `async def`), the `activity_executor` worker parameter must be set to an instance of `concurrent.futures.ThreadPoolExecutor`.

#### Synchronous Multiprocess/Other Activities
If `activity_executor` is set to an instance of `concurrent.futures.Executor` that is not a `ThreadPoolExecutor` (e.g., `ProcessPoolExecutor`), activities are considered multiprocess or other types of activities.

#### Asynchronous Activities
Functions defined with `async def` are asynchronous activities. They are often more performant for I/O-bound operations and do not require any special worker parameters for their execution model within the worker's event loop.

### Worker Concurrency Parameters

The `Worker` constructor provides several parameters to fine-tune concurrency and rate limits:

| Parameter Name | Type | Description | Usage/Implications |
|----------------|------|-------------|-------------------|
| `max_concurrent_activities` | `int` | Maximum number of activity tasks that will be given to this worker concurrently. | Directly controls the worker's capacity for parallel activity execution. |
| `max_activities_per_second` | `float` | Limits the number of activities per second that this specific worker will process. | Worker-side rate limiting. Helps manage the load on external resources accessed by activities. |
| `max_task_queue_activities_per_second` | `float` | Sets the maximum number of activities per second that the task queue will dispatch. | Server-side rate limiting. If multiple workers on the same queue have different values set, they will "thrash." |
| `max_cached_workflows` | `int` | Sets the cache size for sticky workflow execution. | Default is 10K. Proper sizing avoids expensive workflow replays when workers die or cache is evicted due to memory pressure. |
| `workflow_task_poller_behavior` | `PollerBehavior` | Specifies the behavior of workflow task polling, including concurrency. | Recommended over deprecated `max_concurrent_workflow_task_polls`. |
| `activity_task_poller_behavior` | `PollerBehavior` | Specifies the behavior of activity task polling, including concurrency. | Recommended over deprecated `max_concurrent_activity_task_polls`. |

### Optimizing Worker Resource Utilization

Effective worker tuning involves balancing resource utilization with responsiveness. A common goal is to utilize approximately 80% of the worker's CPU capacity while ensuring that schedule-to-start latencies remain low.

Properly sizing the `max_cached_workflows` parameter is also vital. This cache stores workflow event histories, allowing workers to avoid replaying the entire history from scratch when processing subsequent workflow tasks for the same workflow.

## 9. Conclusion

Standalone Temporal Python workers are fundamental components for building resilient and scalable distributed applications. This comprehensive guide has detailed the essential aspects of their operation, from connecting to the Temporal Cluster and defining the core business logic in workflows and activities, to managing their lifecycle and configuring concurrency.

The strict determinism requirements for workflow code, enforced by the SDK's sandbox, are not arbitrary limitations but foundational principles that enable Temporal's unique durability and replayability. Similarly, the flexibility to define activities as synchronous or asynchronous, coupled with appropriate executor configurations, empowers developers to integrate diverse computational and I/O-bound tasks effectively.

Effective worker deployment hinges on careful consideration of connection methods, especially the security implications of mTLS for cloud environments. Moreover, meticulous concurrency tuning, including the strategic use of activity executors and precise configuration of worker-side and server-side rate limits, is paramount for optimizing resource utilization and achieving desired throughput.

By embracing these architectural principles and operational best practices, developers can construct robust, fault-tolerant, and highly performant applications on the Temporal platform.
