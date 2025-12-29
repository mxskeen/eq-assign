# X-Ray lib - serializer module
# Handles saving/loading traces to JSON files.

import json
from pathlib import Path
from typing import Union


def save_trace(session, filepath: Union[str, Path]) -> str:
    # Save an X-Ray session trace to a JSON file.
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(session.to_dict(), f, indent=2)
        
    return str(filepath.absolute())


def load_trace(filepath: Union[str, Path]) -> dict:
    # Load an X-Ray trace from a JSON file.
    with open(filepath, 'r') as f:
        return json.load(f)


def list_traces(directory: Union[str, Path]) -> list[dict]:
    # List all trace files in a directory with basic metadata.
    directory = Path(directory)
    traces = []
    
    if not directory.exists():
        return traces
        
    for filepath in directory.glob("*.json"):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                traces.append({
                    "trace_id": data.get("trace_id"),
                    "name": data.get("name"),
                    "filepath": str(filepath),
                    "started_at": data.get("started_at"),
                    "completed_at": data.get("completed_at"),
                    "step_count": len(data.get("steps", []))
                })
        except (json.JSONDecodeError, KeyError):
            continue
            
    return sorted(traces, key=lambda x: x.get("started_at", ""), reverse=True)
