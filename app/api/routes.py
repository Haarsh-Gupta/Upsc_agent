from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import shutil
import os
import uuid

from app.services.agent import AnswerEvaluation
from app.api.dependencies import get_ai_models, AIModels
from app.models.request import RubricRequest, EvaluationRequest
from app.utils.file_handler import cleanup_session , create_temp_session , save_uploaded_files

router = APIRouter()
TEMP_DIR = "temp_uploads"

@router.post("/ocr")
async def ocr_endpoint(
    files: List[UploadFile] = File(...), 
    subject: str = "GS1", 
    marks: int = 10,
    models: AIModels = Depends(get_ai_models)
):  
    # 1. setup session
    session_dir = create_temp_session()

    try:
        # 2. save files
        file_path = await save_uploaded_files(files , session_dir)

        # 3. Ocr logic
        evaluator = AnswerEvaluation(marks , subject , models.flash , models.pro)
        result = evaluator.ocr(file_path)

        if not result:
            raise HTTPException(status_code = 400, detail = "OCR Failed")
        return result
    
    finally:
        cleanup_session(session_dir)

@router.post("/generate-rubric")
async def rubric_endpoint(request: RubricRequest, models: AIModels = Depends(get_ai_models)):
    try:
        evaluator = AnswerEvaluation(request.total_marks, request.subject, models.flash, models.pro)
        return evaluator.keypoint_generator(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate")
async def evaluate_endpoint(request: EvaluationRequest, models: AIModels = Depends(get_ai_models)):
    try:
        evaluator = AnswerEvaluation(request.total_marks, request.subject, models.flash, models.pro)
        return evaluator.feedback(request.rubric, request.student_answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/full_evaluation")
async def full_evaluation_endpoint(
    files: List[UploadFile] = File(...), 
    subject: str = "GS1", 
    marks: int = 15,
    models: AIModels = Depends(get_ai_models)
):
    """
    Orchestrates the entire flow: OCR -> Rubric -> Evaluation
    Returns all intermediate steps to the user.
    """
    session_dir = create_temp_session()
    
    try:
        # 1. Save Files
        file_paths = await save_uploaded_files(files, session_dir)
        
        # 2. Initialize Evaluator
        evaluator = AnswerEvaluation(marks, subject, models.flash, models.pro)
        
        # 3. Step A: OCR
        # ocr_result = evaluator.ocr(file_paths)
        # if not ocr_result:
        #     raise HTTPException(status_code=400, detail="OCR Step Failed. Could not read files.")
            
        # student_question = ocr_result['question']
        # student_answer = ocr_result['answer']
        
        # # 4. Step B: Generate Rubric
        # # Note: If OCR failed to get a question, we might want to fail early
        # if not student_question:
        #      raise HTTPException(status_code=400, detail="OCR extracted empty question.")

        # rubric_result = evaluator.keypoint_generator(student_question)
        
        # # 5. Step C: Evaluate
        # feedback_result = evaluator.feedback(rubric_result, student_answer)

        response = evaluator.full_evaluation(file_paths)
        return response
        
        # 6. Return Composite Response
        # return {
        #     "status": "success",
        #     "ocr": ocr_result,
        #     "rubric": rubric_result,
        #     "feedback": feedback_result
        # }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        cleanup_session(session_dir)