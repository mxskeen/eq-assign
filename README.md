# X-Ray

A debugging library for multi-step algorithmic systems. Captures decision context at each pipeline step.

## Quick Start

```bash
# Install dependencies
poetry install

# Run demo
poetry run xray-demo

# Start dashboard
cd dashboard && npm install && npm run dev
```

Open http://localhost:5173 to view the trace.

## Project Structure

```
xray/           # Core library
  core.py       # XRaySession, Step, Evaluation, FilterResult
  serializer.py # JSON save/load

demo/           # Demo application
  competitor_selection.py  # 3-step pipeline
  mock_data.py  # Sample products

dashboard/      # React visualization
```

## Usage

```python
from xray import XRaySession, FilterResult, Evaluation

with XRaySession(name="my_pipeline") as session:
    with session.step("filter_step", step_type="filter") as step:
        step.set_input({"candidates": 50})
        
        # Process and capture evaluations
        for candidate in candidates:
            evaluation = Evaluation(candidate_id=candidate["id"], candidate_data=candidate)
            evaluation.add_filter_result(FilterResult(
                filter_name="price_range",
                passed=True,
                detail="INR 749 is within range"
            ))
            step.add_evaluation(evaluation)
        
        step.set_output({"passed": 26})
        step.set_reasoning("Applied price and rating filters")
```

## Key Classes

Classes and their purposes:

`XRaySession` Wraps pipeline execution 
`Step` One stage with input/output/reasoning 
`Evaluation` Per-candidate filter results 
`FilterResult` Pass/fail with detailed reason
