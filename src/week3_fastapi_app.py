from fastapi import FastAPI, BackgroundTasks, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import time

app = FastAPI(title="AI Contract Intelligence API", version="1.0")

# Allow frontend to talk to backend
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

UPLOAD_DIR = "./data/full_contract_pdf"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Simulated in-memory database to store processing statuses
job_status_db = {}

def process_contract_heavy_task(job_id: str, file_path: str):
    """Runs in the background so the API stays lightning fast!"""
    job_status_db[job_id] = "PROCESSING (Running OCR & RoBERTa...)"
    time.sleep(5)  # Simulating your 63 sliding window chunks executing
    
    # Simulating finding a risky auto-renewal clause
    job_status_db[job_id] = {
        "status": "COMPLETED",
        "contract_file": os.path.basename(file_path),
        "total_chunks_analyzed": 63,
        "high_risk_flags": ["HIGH RISK: Auto-renewal clause detected."],
        "extracted_clauses": {
            "Renewal Term": "The agreement will automatically renew for consecutive 2-year terms.",
            "Governing Law": "State of Delaware"
        }
    }

@app.post("/api/v1/analyze-contract/")
async def upload_and_analyze(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported!")
        
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    job_id = f"job_{int(time.time())}"
    job_status_db[job_id] = "QUEUED"
    
    # Trigger AI inference asynchronously
    background_tasks.add_task(process_contract_heavy_task, job_id, file_path)
    
    return {"message": "File successfully uploaded! Inference started.", "job_id": job_id}

@app.get("/api/v1/job-status/{job_id}")
async def get_status(job_id: str):
    if job_id not in job_status_db:
        raise HTTPException(status_code=404, detail="Job ID not found")
    return {"job_id": job_id, "result": job_status_db[job_id]}
