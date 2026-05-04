# External Agents Launch Guide

This folder contains the local clones of the agents mentioned in the reference papers. Most Python agents use the shared environment:

```powershell
$ROOT = "C:\Users\Anwender\Science-Work-Flow-"
$AGENTS = "$ROOT\.venv-agents"
cd $ROOT
```

Check it:

```powershell
& "$AGENTS\Scripts\python.exe" -m pip check
```

LeanDojo is different: it is installed in the Python 3.11 GPU environment because LeanDojo does not support Python 3.13.

```powershell
$LEAN_GPU = "C:\Users\Anwender\AppData\Local\anaconda3\envs\pytorch-gpu"
& "$LEAN_GPU\python.exe" -c "import lean_dojo, torch; print('LeanDojo OK'); print(torch.__version__); print(torch.cuda.is_available())"
```

## Smoke-Test Status (2026-05-04)

These checks were run on this computer from the commands in this guide. Long-running GUI/server commands and token-spending model tasks were not kept running.

| Agent / component | Status | What was verified |
| --- | --- | --- |
| Shared `.venv-agents` | PASS | `python -m pip check` reports no broken requirements. |
| Denario | PASS | CLI help and `from denario import Denario` import work. The GUI launch command starts the Streamlit app when you want to use it. |
| CMBAgent | PASS | `import cmbagent` works from the shared environment. Real tasks require model credentials. |
| AG2 / AutoGen | PASS | `AssistantAgent`, `UserProxyAgent`, and `LLMConfig` import successfully. Real runs need `OAI_CONFIG_LIST`. |
| OpenGauss / Gauss | PASS WITH SETUP | `run-gauss.cmd doctor` launches against `C:\Users\Anwender\LEANCOURSE\LeanCourse25`. It still warns about missing API/login setup; run `gauss setup` for model-backed use. |
| RepoProver | PASS WITH SETUP | CLI help works. The toy Lean project setup, `lake update`, and `lake build` were verified. Full `repoprover run` needs credentials and creates the RepoProver run state. |
| LeanDojo | PASS WITH SETUP | Import, package version, PyTorch `2.9.1+cu128`, CUDA availability, `elan`, and pip check work in the Python 3.11 GPU environment. Full tracing still needs `wget` and `GITHUB_ACCESS_TOKEN`; WSL is preferred for heavy tracing. |
| PDA | PASS | FormL4 data, prompts, annotations, and code folders are present. The paper repo does not release full training/evaluation code. |
| JFC | BLOCKED | `pixi` and `claude` are not on PATH, so the full JFC workflow cannot launch yet. |
| Lean REPL | PASS | `lake build` completed successfully for `external\lean-repl`. |

## Credentials

Set the keys you need before launching model-backed agents:

```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:ANTHROPIC_API_KEY = "sk-ant-..."
$env:GOOGLE_API_KEY = "..."
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\service-account.json"
$env:GITHUB_ACCESS_TOKEN = "ghp_..."
```

`GITHUB_ACCESS_TOKEN` is especially useful for LeanDojo to avoid GitHub API rate limits.

## Denario

Launch the GUI:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-
& ".\.venv-agents\Scripts\denario.exe" run
```

Usually opens Streamlit on port `8501`.

Minimal import check:

```powershell
& ".\.venv-agents\Scripts\python.exe" -c "from denario import Denario; print('Denario OK')"
```

## CMBAgent

Minimal import check:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-
& ".\.venv-agents\Scripts\python.exe" -c "import cmbagent; print('CMBAgent OK:', cmbagent.__file__)"
```

One-shot task, requires an OpenAI key:

```powershell
& ".\.venv-agents\Scripts\python.exe" -c "import cmbagent; task='''Draw two random numbers and give me their sum'''; cmbagent.one_shot(task, agent='engineer', engineer_model='gpt-4o-mini')"
```

Benchmarks are cloned in:

```text
external\cmbagent-benchmarks
```

## AG2 / AutoGen

AG2 imports as `autogen`.

Create an `OAI_CONFIG_LIST` file outside committed files:

```json
[
  {
    "model": "gpt-5",
    "api_key": "<your OpenAI API key here>"
  }
]
```

Run a minimal agent:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-
& ".\.venv-agents\Scripts\python.exe" -c "from autogen import AssistantAgent, UserProxyAgent, LLMConfig; cfg=LLMConfig.from_json(path='OAI_CONFIG_LIST'); a=AssistantAgent('assistant', llm_config=cfg); u=UserProxyAgent('user_proxy', code_execution_config={'work_dir':'coding','use_docker':False}); u.run(a, message='Summarize Python lists vs tuples.').process()"
```

## OpenGauss / Gauss Lean Agent

Use the launcher in `external\OpenGauss`, not raw `gauss.exe`.

Doctor:

```powershell
cd C:\Users\Anwender\LEANCOURSE\LeanCourse25
C:\Users\Anwender\Science-Work-Flow-\external\OpenGauss\run-gauss.cmd doctor
```

Launch:

```powershell
cd C:\Users\Anwender\LEANCOURSE\LeanCourse25
C:\Users\Anwender\Science-Work-Flow-\external\OpenGauss\run-gauss.cmd
```

Inside Gauss:

```text
/chat
/project use C:\Users\Anwender\LEANCOURSE\LeanCourse25
/prove
/autoprove
/formalize
/autoformalize
/swarm
```

## RepoProver

CLI help:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-
& ".\.venv-agents\Scripts\python.exe" -m repoprover --help
```

Run on a prepared Lean project:

```powershell
& ".\.venv-agents\Scripts\python.exe" -m repoprover run C:\path\to\lean\project --pool-size 10
```

RepoProver expects the Lean project to have:

- working Lake/Mathlib setup
- `tex/` source material
- `CONTENTS.md`
- `manifest.json`
- Git initialized with a `main` branch

Toy project smoke test is Bash-based. On this computer, Git Bash is installed and this Windows command pattern was verified:

```powershell
& "C:\Program Files\Git\bin\bash.exe" -lc "cd /c/Users/Anwender/Science-Work-Flow-/external/repoprover && bash examples/toy_project/setup.sh /c/tmp/repoprover-toy-test"
```

Then build the generated Lean project from PowerShell:

```powershell
cd C:\tmp\repoprover-toy-test
lake update
lake build
```

After a first RepoProver run has created run state, inspect status with:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-
& ".\.venv-agents\Scripts\python.exe" -m repoprover status C:\tmp\repoprover-toy-test
```

Run the coordinator on the toy project only after model credentials are set:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-
& ".\.venv-agents\Scripts\python.exe" -m repoprover run C:\tmp\repoprover-toy-test --pool-size 2 --verbose
```

Trajectory viewer:

```powershell
& ".\.venv-agents\Scripts\python.exe" -m repoprover.viewer --dir C:\path\to\lean\project\runs --port 8080
```

## LeanDojo

Use the Python 3.11 GPU env:

```powershell
$LEAN_GPU = "C:\Users\Anwender\AppData\Local\anaconda3\envs\pytorch-gpu"
& "$LEAN_GPU\python.exe" -m pip check
& "$LEAN_GPU\python.exe" -c "import importlib.metadata as m; print(m.version('lean-dojo'))"
```

Run notebooks:

```text
external\LeanDojo\scripts\demo-lean4.ipynb
external\LeanDojo\scripts\generate-benchmark-lean4.ipynb
```

Requirements for full LeanDojo tracing:

- `wget`
- `elan`
- Git
- `GITHUB_ACCESS_TOKEN`
- Prefer WSL on Windows for full support.

Current machine status: Python import/CUDA checks pass, `elan` and Git Bash are present, but `wget` and `GITHUB_ACCESS_TOKEN` were missing during the smoke test.

## PDA

PDA currently provides dataset and annotation assets; its README says training/evaluation code and finetuned models are not released yet.

Check the dataset:

```powershell
Get-ChildItem C:\Users\Anwender\Science-Work-Flow-\external\PDA\data\FormL4
```

Useful folders:

```text
external\PDA\data\FormL4
external\PDA\prompt
external\PDA\annotation
external\PDA\code
```

## JFC

JFC needs `pixi` and Claude Code for the full workflow.

Check whether they exist:

```powershell
Get-Command pixi -ErrorAction SilentlyContinue
Get-Command claude -ErrorAction SilentlyContinue
```

Current machine status: both commands returned nothing during the smoke test, so install `pixi` and Claude Code before launching JFC.

When installed, launch:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-\external\jfc
pixi run scaffold analyses\my_analysis --type measurement
cd analyses\my_analysis
pixi install
claude
```

Then edit `.analysis_config` to set `data_dir` and allowed paths.

## Lean REPL

Lean REPL is a Lean/Lake project, not a Python package.

Build:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-\external\lean-repl
lake build
```

Current machine status: `lake build` completed successfully.

It pins:

```text
leanprover/lean4:v4.30.0-rc2
```

## Local Install Inventory

More detailed install metadata is in:

```text
external\AGENT_INSTALLS.md
```

This includes source repos, install status, and known blockers.
