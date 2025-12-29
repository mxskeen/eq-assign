# X-Ray lib - core module
# captures decision context at each pipeline step: inputs, outputs, reasoning, and filter evaluations.

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from enum import Enum
import uuid
import json


class StepStatus(Enum):
    # Pipeline step status.
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class FilterResult:
    # Result of applying a single filter to a candidate.
    filter_name: str
    passed: bool
    detail: str
    expected: Optional[Any] = None
    actual: Optional[Any] = None
    
    def to_dict(self) -> dict:
        return {
            "filter_name": self.filter_name,
            "passed": self.passed,
            "detail": self.detail,
            "expected": self.expected,
            "actual": self.actual
        }


@dataclass
class Evaluation:
    # A candidate being evaluated through filters.
    candidate_id: str
    candidate_data: dict
    filter_results: list[FilterResult] = field(default_factory=list)
    qualified: bool = False
    metadata: dict = field(default_factory=dict)
    
    def add_filter_result(self, result: FilterResult) -> None:
        self.filter_results.append(result)
        
    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "candidate_data": self.candidate_data,
            "filter_results": [fr.to_dict() for fr in self.filter_results],
            "qualified": self.qualified,
            "metadata": self.metadata
        }


@dataclass
class Step:
    # One stage in a multi-step pipeline.
    name: str
    step_type: str = "generic" 
    input_data: Optional[dict] = None
    output_data: Optional[dict] = None
    reasoning: Optional[str] = None
    evaluations: list[Evaluation] = field(default_factory=list)
    status: StepStatus = StepStatus.PENDING
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    
    def set_input(self, data: dict) -> None:
        self.input_data = data
        
    def set_output(self, data: dict) -> None:
        self.output_data = data
        
    def set_reasoning(self, reasoning: str) -> None:
        self.reasoning = reasoning
        
    def add_evaluation(self, evaluation: Evaluation) -> None:
        self.evaluations.append(evaluation)
        
    def start(self) -> None:
        self.status = StepStatus.RUNNING
        self.started_at = datetime.now().isoformat()
        
    def complete(self) -> None:
        self.status = StepStatus.COMPLETED
        self.completed_at = datetime.now().isoformat()
        
    def fail(self, error: str) -> None:
        self.status = StepStatus.FAILED
        self.completed_at = datetime.now().isoformat()
        self.error = error
        
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "step_type": self.step_type,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "reasoning": self.reasoning,
            "evaluations": [e.to_dict() for e in self.evaluations],
            "status": self.status.value,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error,
            "metadata": self.metadata
        }


class XRaySession:
    # Context manager for collecting X-Ray traces from a pipeline execution.
    
    def __init__(self, name: str, metadata: Optional[dict] = None):
        self.trace_id = str(uuid.uuid4())
        self.name = name
        self.steps: list[Step] = []
        self.started_at: Optional[str] = None
        self.completed_at: Optional[str] = None
        self.metadata = metadata or {}
        self._current_step: Optional[Step] = None
        
    def __enter__(self) -> "XRaySession":
        self.started_at = datetime.now().isoformat()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.completed_at = datetime.now().isoformat()
        
    def step(self, name: str, step_type: str = "generic") -> "StepContext":
        return StepContext(self, name, step_type)
        
    def add_step(self, step: Step) -> None:
        self.steps.append(step)
        
    def to_dict(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "name": self.name,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "metadata": self.metadata,
            "steps": [step.to_dict() for step in self.steps]
        }
        
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


class StepContext:
    # Context manager for an individual step within an X-Ray session.
    
    def __init__(self, session: XRaySession, name: str, step_type: str):
        self.session = session
        self.step = Step(name=name, step_type=step_type)
        
    def __enter__(self) -> Step:
        self.step.start()
        return self.step
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.step.fail(str(exc_val))
        else:
            self.step.complete()
        self.session.add_step(self.step)
