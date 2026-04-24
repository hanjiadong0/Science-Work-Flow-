# Lean Physics References

This folder holds Lean-specific background references that support the project's
physics-heavy proposal from the formalization side.

## Core Archive

- `ITPsInPhysicsArchive`: https://github.com/lean-phys-community/ITPsInPhysicsArchive

As of April 24, 2026, GitHub search also surfaces this archive under the
`HEPLean` organization. The repository describes itself as a list of projects
related to interactive theorem provers in physics.

## Why This Belongs In The Project

The proposal is rich in physics background, but the current scaffold mainly
tracks scientific-agent and evaluation papers. This archive adds the missing
Lean-facing layer:

- it gives a survey of theorem-proving work already connected to physics
- it helps identify realistic formalization targets instead of abstract Lean demos
- it creates a bridge between the proposal's physics motivation and the
  OpenGauss or Lean workflow experiments in this repo

## Suggested Layout Idea: Use It As A Reference Atlas

Instead of treating the archive like one more citation, use it as a small
"reference atlas" with three lenses:

- `landscape`: which physics domains already have ITP activity
- `examples`: which projects are concrete models for style, scope, and proof patterns
- `transfer`: which parts of the proposal could later become Lean-backed checks,
  formal constraints, or benchmark extensions

That layout is useful here because the proposal is not only about Lean itself.
It is about trustworthy scientific reasoning. The archive gives a structured way
to connect physics context, formal methods, and evaluation design.
