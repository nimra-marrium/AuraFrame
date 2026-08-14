"""
Visual Analyst Agent - core logic.

Responsibility: Analyze ONE image, return structured visual data.

PRECONDITION:  URL is a reachable, valid image
POSTCONDITION: none required - pure function
"""
from .schemas import VisualAnalystAgentInput, VisualAnalystAgentOutput


def run(data: VisualAnalystAgentInput) -> VisualAnalystAgentOutput:
    """
    TODO: implement.
    This will call the AI API and return structured JSON - no DB needed.
    """
    raise NotImplementedError("Visual Analyst Agent not implemented yet - this is a skeleton")
