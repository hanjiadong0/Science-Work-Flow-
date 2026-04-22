# Trial Evaluation Modes

This document turns the lab proposal into concrete trial modes that can be run in a sensible order.

The proposal is asking for more than a single benchmark score. It wants a framework that can tell us:

- whether the agent can use scientific tools correctly
- whether multi-step reasoning stays reliable over time
- whether retrieval or domain grounding actually helps
- whether failures are numerical, scientific, or reasoning-related

The trial modes below are designed around those goals.

## Recommended Order

1. `01_sanity_baseline`
2. `02_backbone_model_ablation`
3. `03_grounding_ablation`
4. `04_robustness_stress_test`
5. `05_workflow_comparison`
6. `06_failure_taxonomy_audit`

## Mode 1: Sanity Baseline

Config: `configs/experiments/trials/01_sanity_baseline.json`

Purpose:

- verify that the evaluation loop works end to end
- establish a clean reference run before adding stress or ablations

What it tests:

- one-shot precision behavior
- deep-research inference behavior
- a mixed cosmology task that supports both workflows

What to look at:

- numerical accuracy
- posterior consistency
- tool-use accuracy
- physical validity

Why it matters:

This is the control condition. If the baseline is unstable, later comparisons are hard to trust.

## Mode 2: Backbone Model Ablation

Config: `configs/experiments/trials/02_backbone_model_ablation.json`

Purpose:

- isolate the effect of model strength while holding grounding fixed

What it tests:

- `small-baseline-llm`
- `medium-science-llm`
- `frontier-science-llm`

Questions it answers:

- does a stronger model reduce silent numerical errors
- does model size improve calibration as well as raw accuracy
- do better models help equally on one-shot and multi-step tasks

Expected readout:

- stronger models should improve numerical accuracy
- weaker models should show more hallucinated or mismatched tool behavior

## Mode 3: Grounding Ablation

Config: `configs/experiments/trials/03_grounding_ablation.json`

Purpose:

- compare an ungrounded agent against a domain-grounded one

What it tests:

- `plain`
- `retrieval_augmented`

Questions it answers:

- does domain grounding reduce hallucinated tool calls
- does grounding improve scientific correctness, not just verbosity
- is retrieval more useful in deep-research tasks than in one-shot runs

Expected readout:

- grounding should especially help tasks that require priors, interpretation, or literature cues

## Mode 4: Robustness Stress Test

Config: `configs/experiments/trials/04_robustness_stress_test.json`

Purpose:

- test reliability under the exact stressors named in the proposal

Stress conditions:

- `parameter_misconfiguration`
- `missing_data`
- `weak_priors`
- `degenerate_regime`

Questions it answers:

- does the agent fail gracefully when information is incomplete
- does it admit uncertainty when priors become weak
- does it break under parameter degeneracy
- can it detect rather than silently accept bad tool setups

Expected readout:

- stability under perturbation should drop in a measurable way
- deep-research runs should show a higher error-propagation risk under stress

## Mode 5: Workflow Comparison

Config: `configs/experiments/trials/05_workflow_comparison.json`

Purpose:

- compare `one_shot` and `deep_research` on the same scientific target

Why this mode is special:

- the original scaffold compared workflows mostly across different task types
- this mode adds `configs/tasks/cmb_joint_inference.json` so both workflows can be tested on one cosmology-style inference problem

Questions it answers:

- when is multi-step reasoning actually worth the extra complexity
- when does deeper planning improve uncertainty handling
- when do extra steps create new opportunities for compounded failure

Expected readout:

- `deep_research` may improve interpretation and recovery under missing data
- `one_shot` may stay cleaner on tightly scoped numerical tasks

## Mode 6: Failure Taxonomy Audit

Config: `configs/experiments/trials/06_failure_taxonomy_audit.json`

Purpose:

- collect a broad failure set for qualitative inspection and taxonomy building

What it is for:

- populating examples of silent numerical error
- finding physically inconsistent outputs
- exposing reasoning-output mismatch
- measuring error propagation in multi-step runs

Why it matters:

The proposal does not only want average scores. It explicitly asks for a failure taxonomy that can support a paper on reliable AI in science.

## How These Modes Map to the Proposal

- Proposal goal: covered by the full six-mode sequence
- Tool-grounded precision tasks: emphasized in Modes 1, 2, and 4
- Research-driven inference tasks: emphasized in Modes 1, 3, 4, 5, and 6
- Backbone model effects: Mode 2
- Retrieval and domain grounding: Mode 3
- Multi-step robustness: Modes 4 and 5
- Failure taxonomy: Mode 6

## Practical Advice

- Start with Mode 1 so you have a trusted baseline report.
- Run Modes 2 and 3 next to identify the biggest controllable performance drivers.
- Use Mode 4 to surface brittleness before drawing strong conclusions.
- Use Mode 5 when you want to justify whether deep-research style orchestration is worth the cost.
- Use Mode 6 to collect paper-quality case studies and build a failure taxonomy.
