# Trace-Based Architecture Evaluation Research Report

## Executive Answer

Your updated plan makes sense, and it is no longer just a benchmark idea. The strongest thesis is:

> Agent architectures should be evaluated as dynamical systems. Traces are the data, interaction graphs are the measurement instrument, and domain checks define scientific validity.

The local papers support this direction. Scientific-agent systems such as CMBAgent, Denario, JFC, and mephisto already show that multi-agent architectures can do serious scientific work, but their evaluations still lean heavily on final outputs, expert judgement, or system-specific demonstrations. The evaluation surveys argue that output-only benchmarks are too coarse for long-horizon agents. The astrophysics failure paper shows the main risk directly: agents can produce plausible, executable, confident, but wrong scientific results. The Lean paper adds the missing design pattern: use an external verifier to supervise the process, not only the final answer.

The main remaining difficulty is exactly the one you identified: domain-specific environments, rules, ground truth, and evaluation checks. Without those, trace graphs risk becoming elegant behavioral summaries that do not know whether the science is true.

## Corpus Covered

This digest covers the updated local plan file:

- `references/evaluation/Plan by CHATGPT.txt`

It also covers the unique papers in `references/resource`:

- `Interpreting Multi-band Galaxy Observations with Large Language Model-Based Agents` / mephisto, arXiv 2409.14807.
- `Open Source Planning & Control System with Language Agents for Autonomous Scientific Discovery` / CMBAgent, arXiv 2507.07257.
- `The Denario project: Deep knowledge AI agents for scientific discovery`, arXiv 2510.26887.
- `AI Agents Can Already Autonomously Perform Experimental High Energy Physics` / JFC, arXiv 2603.20179.
- `Plausible but Wrong: A case study on Agentic Failures in Astrophysical Workflows`.

The folder contains duplicate copies of several PDFs, so the digest treats duplicate filenames as one paper when their hashes match.

For broader evaluation context, this report also uses the local evaluation and Lean references already in the project:

- `Evaluation and Benchmarking of LLM Agents: A Survey`.
- `Measuring Data Science Automation: A Survey of Evaluation Tools for AI Assistants and Agents`.
- `A Survey on Evaluation of LLM-based Agents`.
- `Process-Driven Autoformalization in Lean 4`.
- `references/lean/README.md`.

The plan also names foundations such as SWE-bench, AgentBench, OpenTelemetry, Langfuse/LangSmith, AgentTrace, TRAIL, HELM, multi-agent communication learning, and RL trajectory evaluation. These are conceptually relevant, but not all are local PDFs in the current corpus, so they should be verified before being used as formal citations.

## Main Synthesis

The papers point to one clear gap: current scientific-agent evaluation is too focused on whether a system produced a final artifact, while the real scientific risk lives inside the trajectory.

CMBAgent shows a strong Planning and Control architecture for autonomous scientific discovery. It uses many specialized agents, planner-reviewer loops, controller dispatch, code execution, failure handling, context agents, retrieval agents, and cost-saving context resets. Its evaluations show that planning/control improves performance, including on DS-1000 and cosmology tasks. But for your proposal, the most important part is not only that it works. It is that it produces rich traces: plans, reviews, code attempts, failures, retries, tool calls, interpreted results, and handoffs.

Denario broadens the target from one scientific workflow to a modular research pipeline: idea generation, literature checking, methods, analysis, paper drafting, and review. This makes it a good example of architecture-level evaluation. The unit of analysis is no longer one answer, but a pipeline of scientific transformations. Expert review is valuable, but expensive and hard to automate. Trace-based evaluation can sit underneath expert review by showing where a result came from.

JFC shows a stricter scientific-agent architecture for high energy physics. It decomposes work into phases, uses orchestration, phase-specific execution agents, review agents, literature retrieval, allowed and forbidden tools, domain conventions, and written artifacts at gates. Its key lesson is that scientific agents need process constraints. The phase gates, review cycles, logs, and artifact handoffs are exactly the kind of structure that a trace-based evaluator can measure.

mephisto shows another architecture type: hypothesis search over astrophysical model fitting. It represents states with observation data, model choices, fitting results, and chi-square information; then it explores hypotheses through a tree, uses memory to avoid repeated work, and distills validated knowledge into an external knowledge base. This is especially close to your graph idea because its behavior is already tree-like. Its scientific lesson is also important: the best numerical fit may be physically implausible, so evaluation must combine metric fit with scientific plausibility.

The astrophysics failure paper supplies the strongest warning. In CMBAgent-style workflows, a system can execute code and return results while silently computing the wrong thing. Its metrics separate execution success from scientific correctness: ESR checks whether valid executable output exists, PAS checks extracted parameter accuracy, NAS checks numerical curve accuracy, and PRS checks posterior recovery. It also evaluates physical plausibility and failure transparency. This is directly useful for your framework because it shows why success rate alone is inadequate.

The Lean autoformalization paper gives the best analogy for improvement. Process-Driven Autoformalization in Lean 4 uses compiler feedback and a process-supervised verifier. Instead of only checking final formal statements, it uses proof attempts and first-error locations to label intermediate correctness. This is a concrete example of process supervision from an external verifier. In your scientific-agent setting, the equivalents are physics constraints, compiler checks, solver checks, posterior checks, unit tests, benchmark ground truth, and domain-specific validators.

## Architecture Comparison Lens

Use the following comparison lens across papers and systems.

| System | Architecture Type | What To Trace | Evaluation Lesson |
| --- | --- | --- | --- |
| CMBAgent | Planning and Control multi-agent system | plans, reviews, controller decisions, code runs, failures, context resets, retrieval calls | architecture beats one-shot in some settings, but needs trajectory diagnostics |
| Denario | modular end-to-end research assistant | idea, literature, methods, analysis, paper, review transitions | scientific work is pipeline-shaped, not answer-shaped |
| JFC | phase-gated autonomous HEP workflow | phase artifacts, review passes, failed cycles, tool use, literature retrieval, unblinding gates | domain conventions and gates are part of the architecture |
| mephisto | self-play and tree-search scientific agent | hypothesis tree, state transitions, chi-square, memory, knowledge updates | traces can reveal exploration quality and physically implausible optimization |
| Astrophysics failures | evaluation case study | successful executions, parameter extraction, numerical deviations, posterior pathologies | silent wrongness is the core failure mode |
| Lean PDA | process-supervised formalization | compiler errors, proof attempts, first error locations, verifier labels | external process feedback can improve model behavior |

This makes architecture, not model identity, the natural comparison unit. A GPT-based system with weak tracing may be less scientifically reliable than a smaller-model system with strong retrieval, gates, verifiers, and failure transparency.

## Proposed Framework Layers

### 1. Execution Layer

Purpose: run heterogeneous agent architectures in controlled scientific environments.

Candidate architectures:

- One-shot baseline.
- Deep research agent.
- CMBAgent-style Planning and Control.
- Denario-style modular research pipeline.
- JFC-style phase-gated workflow.
- mephisto-style hypothesis tree search.
- Lean-style verifier-in-the-loop formal agent.

The important design choice is to evaluate the architecture as a scaffold plus model plus tools plus memory plus retrieval plus gates, not just the LLM.

### 2. Instrumentation Layer

Purpose: observe all interactions externally.

Capture:

- messages;
- tool calls;
- code execution;
- retrieval calls;
- state transitions;
- timestamps;
- retries;
- errors;
- artifacts;
- validator results;
- reviewer decisions;
- causal links between events.

The agent should not be trusted to summarize its own trace. Logging should come from an observer around the runtime, like an OpenTelemetry-style instrumentation layer.

### 3. Trace Standardization Layer

Purpose: convert raw events into a portable schema.

Minimum event fields:

- `trace_id`;
- `run_id`;
- `architecture_id`;
- `agent_id`;
- `role`;
- `event_type`;
- `content_ref`;
- `timestamp`;
- `input_refs`;
- `output_refs`;
- `tool_name`;
- `status`;
- `cost`;
- `domain_check_refs`;
- `causal_parent_ids`.

This lets you compare different architectures even when their internals differ.

### 4. Interaction Graph Construction

Purpose: reconstruct the behavioral graph from traces.

Nodes can be messages, plans, tool calls, code executions, retrieved documents, artifacts, reviewer decisions, and validation results. Edges can represent causality, conversation, dependency, revision, review, and artifact lineage.

Graph measures should include:

- causal depth;
- branching factor;
- retry loops;
- unresolved branches;
- role centrality;
- tool-call clusters;
- dead-end retrieval;
- orphan artifacts;
- reviewer influence;
- plan-to-execution alignment.

This is where your framework becomes architecture-agnostic. CMBAgent, Denario, JFC, mephisto, and Lean-style systems all become graphs even if their implementation details differ.

### 5. Trajectory Evaluation Layer

Purpose: score the run as a trajectory, not only as a final answer.

Useful metrics:

- final task success;
- time and token cost;
- number of steps;
- tool-call efficiency;
- retry count;
- reviewer correction rate;
- retrieval usefulness;
- convergence speed;
- repeated-run variance;
- pass@k or pass^k;
- plan adherence;
- artifact quality over time.

This layer connects the survey literature on agent evaluation with RL-style trajectory evaluation.

### 6. Failure Mode Detection Layer

Purpose: detect architecture-level failure patterns.

Core failure modes:

- silent numerical error;
- physically inconsistent output;
- hallucinated tool call;
- reasoning-output mismatch;
- unsupported scientific claim;
- unreported degeneracy;
- goal drift;
- coordination collapse;
- reasoning loop;
- premature convergence;
- fragmented reasoning;
- failed handoff;
- reviewer rubber-stamping;
- error propagation.

The astrophysics failure paper is central here because it shows that an agent can look successful while being scientifically wrong.

### 7. Architecture Signature Layer

Purpose: summarize architecture behavior across tasks and domains.

A signature vector could include:

- success rate;
- scientific correctness score;
- trace efficiency;
- robustness to perturbation;
- failure transparency;
- self-diagnosis rate;
- reviewer correction rate;
- exploration diversity;
- tool reliability;
- cost profile;
- failure-mode distribution.

This gives you a compact comparison such as:

`P(behavior | architecture, domain)`

That is stronger than asking "which model scored higher?"

### 8. Cross-Domain Evaluation Layer

Purpose: test whether failure topology changes by scientific domain.

Initial domains should be chosen for ground truth quality, not glamour. Start where validators are strongest.

Recommended order:

1. Cosmology/CAMB precision tasks.
2. Astrophysics posterior recovery tasks.
3. Lean/formalization tasks.
4. HEP-style phase-gated analysis tasks.
5. Astronomy SED fitting tasks.
6. Later: biology, chemistry, causal inference, and simulated lab environments.

The practical rule is simple: no domain enters the benchmark unless it has executable checks, reference outputs, or credible expert-review protocol.

## Evaluation Metrics To Use

Separate four metric families.

### A. Output Correctness

Use these to ask whether the final scientific result is right.

- ESR: did it produce executable, valid output?
- PAS: were key parameters correct?
- NAS: did numerical curves match reference results?
- PRS: did posterior inference recover the target posterior?
- physical validity: are constraints and units respected?
- likelihood or fit quality;
- Lean compile success;
- solver or unit-test success;
- expert review score where automation is not enough.

### B. Process Quality

Use these to ask whether the architecture behaved well.

- step count;
- causal depth;
- branching factor;
- retry loops;
- failed handoffs;
- tool-call efficiency;
- retrieval usefulness;
- plan-to-execution consistency;
- review correction rate;
- artifact revision quality;
- context-reset effect;
- memory reuse;
- knowledge-base update usefulness.

### C. Robustness And Reliability

Use these to ask whether the behavior is stable.

- repeated-run variance;
- robustness under perturbation;
- stability under equivalent prompts;
- sensitivity to missing context;
- recovery from tool failure;
- performance under under-constrained tasks;
- pass@k or pass^k;
- calibration between confidence and correctness.

### D. Trust And Failure Transparency

Use these to ask whether the system knows when it is unsafe.

- failure transparency;
- self-diagnosis rate;
- uncertainty honesty;
- degeneracy reporting;
- refusal to overclaim;
- detection of physically implausible results;
- propagation of earlier uncertainty into final claims.

This is the metric family most directly motivated by "Plausible but Wrong."

## Domain Environment Recommendations

### Cosmology/CAMB Precision

This should be the first benchmark family because it already matches the repo and CMBAgent papers.

Rules:

- use known cosmological parameter settings;
- require correct solver parameters;
- require valid numerical output shape;
- require curve match to reference outputs;
- reject hallucinated tool calls.

Checks:

- ESR;
- PAS;
- NAS;
- tool-use accuracy;
- hallucinated tool calls;
- confidence calibration;
- trace efficiency.

### Astrophysics Posterior Recovery

This should test the "plausible but wrong" risk.

Rules:

- specify priors and likelihood assumptions;
- provide synthetic or reference posterior;
- include stress tests with degeneracy or under-constrained observations;
- require explicit uncertainty reporting.

Checks:

- PRS;
- posterior consistency;
- physical plausibility;
- failure transparency;
- whether the trace reveals diagnosis or concealment of degeneracy.

### Astronomy SED Fitting

This fits the mephisto paper.

Rules:

- provide photometric observations;
- define allowed SED model families and priors;
- include known plausible physical regimes;
- do not reward chi-square alone.

Checks:

- chi-square and well-fitted bands;
- physical plausibility;
- hypothesis diversity;
- repeated-attempt avoidance;
- knowledge-base usefulness;
- whether the agent reports degeneracy.

### High Energy Physics

This fits the JFC paper.

Rules:

- encode phase structure;
- require cutflow and background estimation artifacts;
- require systematic uncertainty propagation;
- include closure tests;
- enforce allowed and forbidden tools;
- include unblinding gates where relevant.

Checks:

- phase artifact completeness;
- review pass rate;
- number of review cycles;
- agreement with reference measurement;
- systematic propagation quality;
- trace evidence for domain-convention compliance.

### Lean And Formal Verification

This gives the cleanest external verifier.

Rules:

- Lean code must compile;
- theorem statements must match informal intent;
- proof attempts can be used as auxiliary process evidence;
- first compiler error location should be captured.

Checks:

- compile success;
- first-error location;
- process-supervised correctness labels;
- semantic alignment;
- proof repair trajectory;
- repeated-run stability.

Lean is especially valuable because it shows how to turn process traces into training and improvement signals, not only evaluation signals.

## How This Improves The Existing Repo

The current repo already has the right seeds: task configs, workflow modes, metrics, taxonomy, and a deterministic stub agent. The next improvement is to move from task-level outputs to architecture-level traces.

Recommended MVP:

1. Add trace event models in `src/cambagent_eval/models.py`.
2. Add an external `TraceObserver` that records events without relying on the agent's self-report.
3. Add `graph.py` to construct an interaction graph from standardized events.
4. Extend `metrics.py` with graph/process metrics: loop count, causal depth, tool efficiency, retry rate, orphan artifacts, and reviewer correction rate.
5. Extend `taxonomy.py` with architecture failure modes: coordination collapse, premature convergence, fragmented reasoning, failed handoff, silent numerical error, and reviewer rubber-stamping.
6. Add architecture configs, separate from model configs.
7. Add a report generator that outputs an architecture signature vector and a failure-mode profile.
8. Run first on the current one-shot and deep-research stub workflows, then connect to real CMBAgent/OpenGauss adapters.

This MVP would make the proposal concrete without requiring a full new agent.

## Short Verdict

Yes, the plan is scientifically and architecturally strong. Its best contribution is not another benchmark, but a method for measuring how scientific-agent architectures behave.

The paper corpus supports three claims:

1. Scientific agents are becoming capable enough that architecture matters.
2. Existing evaluations miss important trajectory-level failure modes.
3. Scientific validity needs external checks, verifiers, and domain rules.

The key risk is weak environments. If the domain checks are shallow, the graph metrics will look sophisticated but will not protect against wrong science. The strongest version of the project starts with domains where ground truth and validators are already available, then expands outward.

The compressed research question should be:

> How can we evaluate scientific-agent architectures by reconstructing their interaction traces into behavioral graphs and measuring success, efficiency, robustness, and failure modes under domain-specific scientific validators?
