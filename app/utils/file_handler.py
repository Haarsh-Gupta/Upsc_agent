import os 
import shutil
import uuid
from fastapi import UploadFile
from typing import List, Tuple 

#Temp_dir
TEMP_DIR = "temp_uploads" 

def create_temp_session() -> str:
    """Creates a unique directory for this request session."""
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(TEMP_DIR , session_id)
    os.makedirs(session_dir, exist_ok = True)
    return session_dir

async def save_uploaded_files(files: List[UploadFile] , session_dir: str) -> List[str] :
    """Saves uploaded files to the session directory and returns their paths."""
    saved_paths = []
    for file in files:
        file_path = os.path.join(session_dir , file.filename) 

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file , buffer)

        saved_paths.append(file_path)
        return saved_paths
    
def cleanup_session(session_dir: str):
    """Deletes the session directory and all files inside."""
    if os.path.exists(session_dir):
        shutil.rmtree(session_dir)
    