# Financial Document Analyzer - Debug Assignment

## Project Overview
A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents. The system now supports concurrent requests via a Celery queue (Redis backend) and stores results in a database for persistence.

## Getting Started

### Sample Document
The system analyzes financial documents like Tesla's Q2 2025 financial update.

**To add Tesla's financial document:**
1. Download the Tesla Q2 2025 update from: https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf
2. Save it as `data/sample.pdf` in the project directory
3. Or upload any financial PDF through the API endpoint

### Setup Instructions

1. Create Virtual Environment
```bash
python -m venv venv
```

2. Activate Virtual Environment
Windows:
```bash
venv\Scripts\activate
```
Linux/Mac:
```bash
source venv/bin/activate
```

3. Install Requirements
```bash
pip install -r requirements.txt
```

4. Setup Redis
```bash
docker run -d -p 6380:6379 redis
```

5. Start the Celery Worker
```bash
celery -A celery_app.celery_app worker --loglevel=info
```

6. Run the Application
```bash
uvicorn main:app --reload --port 8000
```

### Bugs Found & Fixes

1. Requirements Version Mismatch
* Updated `requirements.txt` to compatible versions for all libraries.

2. Missing/Incorrect Imports
* Fixed missing `PyPDFLoader` import and removed unused imports like `asyncio`.

3. LLM Placeholder Issue
* Replaced placeholder `llm = llm` with actual LLM initialization.

4. Improper Class/Tool Usage
* Changed `FinancialDocumentTool.read_data_tool` from raw class reference to instance method: `FinancialDocumentTool().read_data_tool()`.

5. Async Misuse & Inefficiencies
* Removed unnecessary `async` in class methods.
* Simplified double-space removal logic in PDF processing.

6. Agent & Task Mismatches
* Assigned correct agents to tasks (e.g., `verifier` handles verification).
* Removed hallucination/instruction errors in prompts; made backstories professional and realistic.
* Fixed flow: verify → analyze → recommend → assess risk.

7. Prompting & Output Issues
* Fixed misleading prompts that caused hallucinations.
* Ensured outputs are structured, clear, and realistic.

8. FastAPI Route Conflicts
* Renamed route function to avoid overwriting imported `analyze_financial_document` task.

9. Pipeline & File Handling
* Updated Crew pipeline to include all agents/tasks sequentially.
* Ensured PDF `file_path` is correctly passed to tools/tasks for analysis.

10. Other Minor Fixes
* Removed unnecessary imports and clarified tool usage.

### API Documentation

**Base URL:** `http://localhost:8000/`  

### **Endpoints**

### 1. Health Check
**GET /**  
**Description:** Verify that the API is running.  
**Response:**
```json
{
  "message": "Financial Document Analyzer API with Queue is running"
}
```

## 2. Queue Financial Document Analysis

**POST** `/analyze`  

**Description:** Upload a PDF document and queue it for analysis.  

**Form Data:**

- `file` (UploadFile, required): Financial PDF document.  
- `query` (str, optional): Analysis instruction. Defaults to `"Analyze this financial document for investment insights"`.  

**Response Example:**
```json
{
  "status": "queued",
  "task_id": "UUID",
  "celery_task_id": "CeleryTaskID",
  "query": "Analyze this financial document for investment insights",
  "file_processed": "document.pdf",
  "message": "Analysis queued successfully. Use /status/{task_id} to check progress."
}
```

### 3. Check Task Status

**GET** `/status/{task_id}`  

**Description:** Retrieve the status and result of a queued analysis task.  

**Path Parameters:**

- `task_id` (str): ID of the task to check.  

**Response Example (Pending Task):**
```json
{
  "task_id": "UUID",
  "status": "pending",
  "query": "Analyze this financial document for investment insights",
  "file_name": "document.pdf",
  "result": null,
  "created_at": "2025-09-18T12:00:00"
}
```
**Response Example (Completed Task):**
```json
{
  "task_id": "UUID",
  "status": "completed",
  "query": "Analyze this financial document for investment insights",
  "file_name": "document.pdf",
  "result": "Structured analysis results here...",
  "created_at": "2025-09-18T12:00:00"
}
```

**4. List Recent Results**

**GET /results**  
**Description:** List the most recent analysis results.

**Query Parameters:**

- `limit` (int, optional, default=10): Number of results to return.

**Response Example:**
```json
{
  "results": [
    {
      "task_id": "UUID1",
      "status": "completed",
      "query": "Analyze this financial document for investment insights",
      "file_name": "document1.pdf",
      "created_at": "2025-09-18T12:00:00"
    },
    {
      "task_id": "UUID2",
      "status": "pending",
      "query": "Check investment risk factors",
      "file_name": "document2.pdf",
      "created_at": "2025-09-18T11:50:00"
    }
  ]
}
```

**5. Delete Analysis Result**

**DELETE /results/{task_id}**  
**Description:** Delete a previously stored analysis result.

**Path Parameters:**

- `task_id` (str): ID of the result to delete.

**Response Example:**
```json
{
  "message": "Result deleted successfully"
}
```

**6. Queue Status**

**GET /queue/status**  
**Description:** Retrieve the status of the Celery queue and currently active tasks.

**Response Example:**
```json
{
  "active_tasks": {...},
  "queue_length": {...},
  "broker_url": "redis://localhost:6379/0"
}
```
**Notes:**

- Shows number of active and reserved tasks in the queue.  
- Useful for monitoring concurrent processing.  

### System Upgrades Included:

- **Queue Worker Model:** Added Celery + Redis to handle concurrent requests efficiently.  
- **Database Integration:** SQLite used to store analysis results and user data.  
- **Structured Flow:** Tasks now follow professional sequence: verify → analyze → investment recommendation → risk assessment.  
- **Agent Improvements:** Specialized agents used to avoid hallucinations and produce clear, realistic outputs.  
- **Error Handling:** File validation, queue exceptions, and database errors handled gracefully.  
