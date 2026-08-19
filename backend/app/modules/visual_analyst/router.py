from fastapi import APIRouter

from .schemas import VisualAnalystInput, VisualAnalystOutput
from .service import run

router = APIRouter()


@router.post("/", response_model=VisualAnalystOutput)
def analyze_visual(data: VisualAnalystInput):
    return run(data)