from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from sqlalchemy.orm import Session
import os
import uuid
from database.models import init_db, get_db, AnalysisResult
from celery_tasks import analyze_document_task
from celery_app import celery_app
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # initialize database
    yield

app = FastAPI(title="Financial Document Analyzer with Queue", lifespan=lifespan)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API with Queue is running"}

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
    db: Session = Depends(get_db)
):
    """Queue financial document analysis"""
    
    task_id = str(uuid.uuid4())
    file_id = str(uuid.uuid4())
    file_path = f"output/financial_document_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"
        
        db_result = AnalysisResult(
            id=task_id,
            query=query.strip(),
            file_name=file.filename,
            result="Processing...",
            status="pending"
        )
        db.add(db_result)
        db.commit()
        
        celery_task = analyze_document_task.delay(task_id, query.strip(), file_path, file.filename)
        
        return {
            "status": "queued",
            "task_id": task_id,
            "celery_task_id": celery_task.id,
            "query": query,
            "file_processed": file.filename,
            "message": "Analysis queued successfully. Use /status/{task_id} to check progress."
        }
        
    except Exception as e:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Error queueing analysis: {str(e)}")

@app.get("/status/{task_id}")
async def get_analysis_status(task_id: str, db: Session = Depends(get_db)):
    result = db.query(AnalysisResult).filter(AnalysisResult.id == task_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "task_id": task_id,
        "status": result.status,
        "query": result.query,
        "file_name": result.file_name,
        "result": result.result if result.status == "completed" else None,
        "created_at": result.created_at
    }

@app.get("/results")
async def list_results(limit: int = 10, db: Session = Depends(get_db)):
    results = db.query(AnalysisResult).order_by(
        AnalysisResult.created_at.desc()
    ).limit(limit).all()
    
    return {
        "results": [
            {
                "task_id": r.id,
                "status": r.status,
                "query": r.query,
                "file_name": r.file_name,
                "created_at": r.created_at
            }
            for r in results
        ]
    }

@app.delete("/results/{task_id}")
async def delete_result(task_id: str, db: Session = Depends(get_db)):
    result = db.query(AnalysisResult).filter(AnalysisResult.id == task_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(result)
    db.commit()
    return {"message": "Result deleted successfully"}

@app.get("/queue/status")
async def queue_status():
    try:
        active_tasks = celery_app.control.inspect().active()
        queue_length = celery_app.control.inspect().reserved()
        return {
            "active_tasks": active_tasks,
            "queue_length": queue_length,
            "broker_url": celery_app.conf.broker_url
        }
    except Exception as e:
        return {
            "error": f"Could not fetch queue status: {str(e)}",
            "broker_url": celery_app.conf.broker_url
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
