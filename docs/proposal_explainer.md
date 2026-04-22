# Cambagent Lab Proposal Explainer

This is a plain-language explanation of the proposal in `Cambagent_lab_proposal.pdf`.

## One-Sentence Summary

The proposal is about building a careful test framework for scientific AI agents so we can measure not only whether they finish a task, but whether they reason correctly, use tools correctly, and stay scientifically trustworthy.

## The Big Problem

The proposal starts from a real concern: scientific AI agents can look impressive on demos, but that does not mean they are reliable enough for research.

In science, a system can fail in ways that are subtle:

- it can call the wrong tool but still produce plausible-looking text
- it can produce numerically wrong results without obvious warnings
- it can make a scientifically invalid conclusion even if the final answer sounds confident
- small early mistakes can compound across a multi-step workflow

So the proposal is not trying to prove that agents are useful in general. It is trying to measure when they are trustworthy and when they are not.

## The Main Goal

The goal is to build a structured evaluation framework for LLM-based agentic systems in scientific workflows.

That means:

- define scientific tasks with known answers or strong reference behavior
- run agents under controlled conditions
- compare different models, workflow styles, and grounding setups
- measure failures in a systematic way

The proposal chooses astrophysical inference as the testbed because it is scientifically rich, numerically demanding, and full of physically meaningful constraints.

## Why Astrophysics Is a Good Testbed

Astrophysics is useful here because it combines:

- hard numerical computation
- domain knowledge
- uncertainty quantification
- interpretation of results

That makes it a strong stress test for scientific agents. A model cannot rely only on fluent language. It also has to respect equations, priors, parameter ranges, and physical meaning.

## The Two Task Families

The proposal separates the benchmark into two task families.

### 1. Tool-Grounded Precision Tasks

These are focused numerical tasks where the main question is whether the agent can correctly use scientific tools such as CAMB-like solvers.

The proposal wants to evaluate:

- tool invocation correctness
- parameter configuration
- numerical accuracy

In simple terms, this asks: can the agent use the right scientific software in the right way and get the right numbers out?

### 2. Research-Driven Inference Tasks

These are harder tasks that look more like actual scientific reasoning.

They involve:

- Bayesian inference
- multi-step reasoning
- interpreting uncertainty

In simple terms, this asks: can the agent work through a more realistic scientific problem where it must plan, infer, and explain results under uncertainty?

## What "One-Shot" and "Deep Research" Mean

The proposal compares two workflow styles.

### One-Shot Workflows

These are short, direct runs. The agent gets the task, uses a tool if needed, and produces an answer quickly.

Best for:

- tightly scoped numerical jobs
- fast precision checks
- tasks with little need for planning or retrieval

Risk:

- the agent may skip validation or context gathering

### Deep Research Workflows

These are multi-step workflows where the agent plans, retrieves context, runs inference, and then interprets the result.

Best for:

- open-ended research tasks
- uncertainty-sensitive inference
- tasks that depend on prior knowledge or literature context

Risk:

- each extra step creates another place where errors can appear or compound

## What You Are Actually Supposed to Build

The proposal does not ask for a new scientific agent from scratch.

Instead, it asks for a modular evaluation and ablation pipeline. That means a framework where you can swap parts in and out and study how the system changes.

The three main ablation directions are:

### 1. Backbone Model Effects

You change the underlying LLM and see what happens.

This tests whether improvements come from:

- larger models
- better reasoning ability
- better tool use
- better numerical reliability

### 2. Retrieval or Domain Grounding

You compare:

- a grounded agent with scientific context
- a plain LLM without that support

This tests whether domain grounding reduces:

- hallucinated API calls
- scientifically wrong conclusions
- misuse of tools or priors

### 3. Multi-Step Reasoning Robustness

You deliberately make the task harder by adding realistic stress.

The proposal specifically names:

- missing or incomplete data
- weak or absent priors
- degenerate parameter regimes

This tests whether the agent remains careful under uncertainty or starts to drift into confident but unreliable outputs.

## The Core Research Questions

The proposal is really asking five big questions.

### Where do agents fail?

Important failure types named in the proposal:

- silent numerical errors
- physically inconsistent conclusions
- reasoning-output mismatch

This means the agent may sound reasonable while still being wrong in different scientific ways.

### Which components matter most?

This is about separating the effects of:

- model size
- architecture
- retrieval or grounding

The idea is to learn which design choices genuinely improve reliability.

### How robust are multi-step pipelines?

This is the error compounding question.

If an agent makes a small mistake in planning or retrieval, does that mistake later distort inference and final interpretation?

### Can we build a failure taxonomy?

A failure taxonomy is just a structured set of failure categories.

Instead of saying "the agent failed," you want to say exactly how it failed and whether that pattern repeats across tasks.

### Do improvements generalize?

An improvement that helps one benchmark but fails elsewhere is not enough.

The proposal wants to know whether gains carry across:

- task types
- workflow types
- ablation settings

## How the Proposal Says to Evaluate Performance

The proposal recommends both quantitative and qualitative evaluation.

### Quantitative Metrics

The PDF explicitly names:

- deviation from known ground-truth parameters
- consistency of inferred posteriors
- likelihood fit
- stability under perturbations
- error propagation across steps

In plain language:

- are the numbers right
- are the uncertainty estimates coherent
- does the solution stay stable when the problem gets harder

### Qualitative Analysis

The proposal also wants failure-case analysis.

This is important because two systems can have similar average scores but fail in very different ways. One may make honest low-confidence errors, while another may produce polished but scientifically invalid answers.

## Expected Outcome

By the end of the project, the proposal expects four major outputs:

1. A systematic evaluation framework for scientific agents.
2. A taxonomy of failure modes.
3. Practical insight into when these systems can be trusted and when they break down.
4. A strong basis for a research paper on reliability in AI-for-science.

So the deliverable is both technical and research-oriented. It should produce reusable infrastructure and publishable scientific insight.

## What the Cited Materials Contribute

The proposal lists three important references. They play different roles.

### 1. `arXiv:2603.20179`

Link: https://arxiv.org/abs/2603.20179

Paper title:

- `AI Agents Can Already Autonomously Perform Experimental High Energy Physics`

Why it matters:

- shows that agents can already automate substantial parts of a real scientific workflow
- strengthens the proposal's motivation that capability is no longer the only question
- supports the need for careful validation, because powerful agents can be used before they are well understood

### 2. `arXiv:2507.07257`

Link: https://arxiv.org/abs/2507.07257

Paper title:

- `Open Source Planning & Control System with Language Agents for Autonomous Scientific Discovery`

Why it matters:

- introduces `cmbagent`, a multi-agent scientific system directly related to the proposal
- shows a planning-and-control style architecture with specialized agents
- provides the clearest architectural inspiration for the proposal's "CMBAgent-like systems"

### 3. `arXiv:2510.26887`

Link: https://arxiv.org/abs/2510.26887

Paper title:

- `The Denario project: Deep knowledge AI agents for scientific discovery`

Why it matters:

- extends the picture from one scientific workflow to a broader research assistant model
- emphasizes expert evaluation, review-style feedback, and cross-disciplinary use
- reinforces the proposal's focus on strengths, weaknesses, and limitations rather than hype

## Simple Mental Model

If you want the proposal in one practical sentence:

- build a benchmark lab for scientific agents, then stress the agents until you understand exactly how they fail

That is the central idea.

## How This Repo Maps to the Proposal

The current scaffold already reflects the proposal at a high level:

- `configs/tasks/` stores benchmark task definitions
- `configs/experiments/` stores experiment matrices
- `src/cambagent_eval/metrics.py` computes quantitative metrics
- `src/cambagent_eval/taxonomy.py` labels failure modes
- `src/cambagent_eval/workflows.py` distinguishes one-shot and deep-research traces

The new trial-mode configs under `configs/experiments/trials/` make that mapping more explicit and easier to run in stages.
