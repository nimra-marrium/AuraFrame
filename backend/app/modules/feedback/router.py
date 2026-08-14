"""
Feedback/Eval - HTTP interface. Stays THIN - delegates to service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import FeedbackEvalInput, FeedbackEvalOutput
from . import service

router = APIRouter()


@router.post("/", response_model=FeedbackEvalOutput)
def handle_feedback(payload: FeedbackEvalInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Feedback/Eval not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
