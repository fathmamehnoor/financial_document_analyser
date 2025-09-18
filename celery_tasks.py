import os
from celery_app import celery_app
from database.models import SessionLocal, AnalysisResult
from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # ensure output folder exists

@celery_app.task
def analyze_document_task(task_id: str, query: str, file_path: str, file_name: str):
    """Celery task to analyze financial documents and save results to output folder"""
    db = SessionLocal()
    
    try:
        # Update status to processing
        result = db.query(AnalysisResult).filter(AnalysisResult.id == task_id).first()
        if result:
            result.status = "processing"
            db.commit()
        
        # Run the crew analysis
        crew = Crew(
            agents=[financial_analyst],
            tasks=[analyze_financial_document],
            process=Process.sequential,
        )
        
        analysis_result = crew.kickoff({'query': query, 'file_path': file_path})
        analysis_text = str(analysis_result)
        
        # Save result to output folder
        output_file_name = f"analysis_{file_name.replace('.pdf','')}_{task_id}.txt"
        output_file_path = os.path.join(OUTPUT_DIR, output_file_name)
        with open(output_file_path, "w") as f:
            f.write(analysis_text)
        
        # Update database with path to output file
        if result:
            result.result = output_file_path  # store the path instead of raw text
            result.status = "completed"
            db.commit()
        
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return output_file_path
        
    except Exception as e:
        # Update status to failed
        if result:
            result.status = "failed"
            result.result = f"Error: {str(e)}"
            db.commit()
        raise e
    
    finally:
        db.close()
