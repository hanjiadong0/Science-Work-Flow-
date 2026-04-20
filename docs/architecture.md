# Architecture Notes

The scaffold is organized around the evaluation questions in the lab proposal rather than around a single model backend.

## Core Concepts

- `TaskCase`: a benchmark item with ground truth, expected tools, priors, and domain context
- `ExperimentSpec`: an evaluation matrix over models, grounding modes, workflows, and stress tests
- `StubScientificAgent`: a deterministic adapter that simulates an agent run so the framework is testable offline
- `RunResult`: one execution of one task under one experimental condition
- `ExperimentReport`: aggregated results plus summary statistics and a failure taxonomy

## Module Map

- [models.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/models.py): shared dataclasses
- [config.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/config.py): loading and validation for JSON configs
- [agents.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/agents.py): agent adapter layer
- [workflows.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/workflows.py): trace construction for one-shot and deep-research workflows
- [metrics.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/metrics.py): quantitative scoring
- [taxonomy.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/taxonomy.py): failure-mode classification
- [pipeline.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/pipeline.py): run planning, execution, aggregation, and report writing
- [cli.py](/c:/Users/Anwender/Science-Work-Flow-/src/cambagent_eval/cli.py): command-line entry point

## Extension Points

To move from scaffold to research-grade system:

1. Implement a real adapter that subclasses `AgentAdapter` or follows the same `run(...)` contract.
2. Add benchmark loaders for synthetic or observational datasets.
3. Persist traces, tool arguments, and retrieved evidence so failure analysis can be audited after the fact.
4. Add plotting notebooks or scripts that consume the JSON reports in `outputs/`.

