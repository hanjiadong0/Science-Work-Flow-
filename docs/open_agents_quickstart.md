# Two-Agent Quickstart

Run both agents from:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-
```

## 1. CMBAgent

Check that CMBAgent is ready:

```powershell
cmd /c external\cmbagent\run-cmbagent.cmd doctor
```

Run a real one-shot task:

```powershell
cmd /c external\cmbagent\run-cmbagent.cmd one-shot "Explain three pre-run checks for a flat LCDM CAMB run."
```

Run a deeper planning task:

```powershell
cmd /c external\cmbagent\run-cmbagent.cmd deep-research "Design a short evaluation plan for a CAMB parameter-inference workflow."
```

CMBAgent is task-first. You usually open it by sending a task directly.

## 2. OpenGauss

The current Lean experiment project for OpenGauss is:

- local path in this repo: `C:\Users\Anwender\Science-Work-Flow-\projects\LeanCourse25`
- real clone target: `C:\Users\Anwender\LEANCOURSE\LeanCourse25`
- git remote: `git@github.com:hanjiadong0/LeanCourse25.git`
- launcher: `external\OpenGauss\run-gauss-lean25.cmd`

Check that OpenGauss is ready:

```powershell
cmd /c external\OpenGauss\run-gauss-lean25.cmd doctor
```

Open the interactive Gauss shell:

```powershell
cmd /c external\OpenGauss\run-gauss-lean25.cmd
```

Then inside Gauss, type for example:

```text
/chat
/formalize "Translate a short math statement into Lean."
/autoformalize "Formalize a simple theorem from the current Lean project."
```

Or run one direct project-aware query:

```powershell
cmd /c external\OpenGauss\run-gauss-lean25.cmd chat -Q -q "What Lean project am I in?"
```

OpenGauss is project-first. You usually open it and then type slash commands inside the Lean project.

If you want to browse the Lean files from this repo folder, open:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-\projects\LeanCourse25
```

## Shared Python Env

Both launchers now prefer the shared repo-level environment:

- `C:\Users\Anwender\Science-Work-Flow-\.venv-agents`

That means these same commands use one Python installation for both agents.
