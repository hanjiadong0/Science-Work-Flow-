# Local Agent Runbook

Date: 2026-05-04

This is the local run guide for the agent systems cloned under `external`. The cloned repos themselves are ignored by Git, so this document is the pushable record of how this computer is wired.

## Machine Layout

Main paths:

```powershell
$SWF = "C:\Users\Anwender\Science-Work-Flow-"
$AGENTS = "C:\Users\Anwender\Science-Work-Flow-\.venv-agents"
$LEAN_MAIN = "C:\Users\Anwender\LEANCOURSE\LeanCourse25"
$LEAN_GPU = "C:\Users\Anwender\AppData\Local\anaconda3\envs\pytorch-gpu"
```

Python environments:

| Use | Python | Path | Status |
| --- | --- | --- | --- |
| General scientific agents | 3.13.5 | `.venv-agents` | Used for AG2, CMBAgent, Denario, DenarioApp, JFC package, OpenGauss, PDA deps, RepoProver |
| LeanDojo GPU environment | 3.11.14 | `C:\Users\Anwender\AppData\Local\anaconda3\envs\pytorch-gpu` | Used for LeanDojo because LeanDojo requires `Python >=3.9,<3.13` |

Verified package versions:

```text
ag2==0.12.2
cmbagent==0.0.1.post64
denario==1.0.1
denario-app==1.0.1
slopspec==0.1.0
repoprover==0.1.0
gauss-agent==0.2.2
lean-dojo==4.20.0
torch==2.9.1+cu128
```

Both Python environments pass dependency checks:

```powershell
& "$AGENTS\Scripts\python.exe" -m pip check
& "$LEAN_GPU\python.exe" -m pip check
```

## Credentials

Most agents will start without keys but will not do useful model work until credentials are present.

For the current PowerShell session:

```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:ANTHROPIC_API_KEY = "sk-ant-..."
$env:GOOGLE_API_KEY = "..."
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\service-account.json"
$env:GITHUB_ACCESS_TOKEN = "ghp_..."
```

Notes:

- CMBAgent and Denario primarily need model provider keys.
- PDA uses OpenAI/Vertex AI/Gemini-style dependencies.
- LeanDojo warns when `GITHUB_ACCESS_TOKEN` is missing and can hit GitHub API limits without it.
- OpenGauss has its own setup flow through `run-gauss.cmd doctor` and `run-gauss.cmd setup`.

## General Agent Environment

Use direct commands when possible, because it avoids PowerShell activation-policy surprises.

```powershell
cd C:\Users\Anwender\Science-Work-Flow-
& ".\.venv-agents\Scripts\python.exe" --version
& ".\.venv-agents\Scripts\python.exe" -m pip check
```

To activate:

```powershell
& ".\.venv-agents\Scripts\Activate.ps1"
```

## Denario

Installed from:

```text
external\Denario
external\DenarioApp
external\DenarioExamplePapers
```

Run the local Streamlit GUI:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-
& ".\.venv-agents\Scripts\denario.exe" run
```

The app uses Streamlit, usually on port `8501`.

Minimal Python API pattern:

```powershell
& ".\.venv-agents\Scripts\python.exe" -c "from denario import Denario; den=Denario(project_dir='denario_test_project'); print(den)"
```

For actual research generation, create a project directory with data, set provider keys, then call:

```python
from denario import Denario, Journal

den = Denario(project_dir="project_dir")
den.set_data_description("""
Analyze the experimental data stored in data.csv using sklearn and pandas.
""")
den.get_idea()
den.get_method()
den.get_results()
den.get_paper(journal=Journal.APS)
```

## CMBAgent

Installed from:

```text
external\cmbagent
external\cmbagent-benchmarks
```

Smoke import:

```powershell
& ".\.venv-agents\Scripts\python.exe" -c "import cmbagent; print(cmbagent.__file__)"
```

README one-shot pattern:

```powershell
& ".\.venv-agents\Scripts\python.exe" -c "import cmbagent; task='''Draw two random numbers and give me their sum'''; cmbagent.one_shot(task, agent='engineer', engineer_model='gpt-4o-mini')"
```

Use this only after `OPENAI_API_KEY` is set. Domain extras such as astro/materials/biochem were not installed in this pass.

## AG2

Installed from:

```text
external\ag2
```

AG2 uses the `autogen` import name. Create an `OAI_CONFIG_LIST` file outside committed files, for example:

```json
[
  {
    "model": "gpt-5",
    "api_key": "<your OpenAI API key here>"
  }
]
```

Minimal agent script:

```powershell
& ".\.venv-agents\Scripts\python.exe" -c "from autogen import AssistantAgent, UserProxyAgent, LLMConfig; cfg=LLMConfig.from_json(path='OAI_CONFIG_LIST'); a=AssistantAgent('assistant', llm_config=cfg); u=UserProxyAgent('user_proxy', code_execution_config={'work_dir':'coding','use_docker':False}); u.run(a, message='Summarize Python lists vs tuples.').process()"
```

## OpenGauss / Gauss For Lean

Installed from:

```text
external\OpenGauss
```

Use the local launcher, not the raw `gauss.exe`, because `run-gauss.cmd` sets the intended Gauss home and agent path for this setup.

Doctor from the main Lean source:

```powershell
cd C:\Users\Anwender\LEANCOURSE\LeanCourse25
C:\Users\Anwender\Science-Work-Flow-\external\OpenGauss\run-gauss.cmd doctor
```

Current doctor status:

- Active Lean working directory: `C:\Users\Anwender\LEANCOURSE\LeanCourse25`
- Active Gauss project: `LeanCourse25`
- Managed backend: `codex`
- `lake`, `uvx`, `codex`, `git`, `rg`, Docker, and Node.js are detected.
- Remaining setup: run `gauss setup` if you want API keys/OpenRouter/web tool access.

Start the interactive Lean agent shell:

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

Installed from:

```text
external\repoprover
```

CLI check:

```powershell
& ".\.venv-agents\Scripts\python.exe" -m repoprover --help
```

Main usage pattern from the README:

```powershell
& ".\.venv-agents\Scripts\python.exe" -m repoprover run C:\path\to\lean\project --pool-size 10
```

RepoProver expects a Lean project repository with:

- a working Lake/Mathlib project
- `tex/` source material inside the Lean project
- `CONTENTS.md`
- `manifest.json`
- Git initialized with a `main` branch

For a first small local run, use the included toy project. The setup script is Bash, so run it through WSL or Git Bash:

```bash
cd /mnt/c/Users/Anwender/Science-Work-Flow-/external/repoprover
bash examples/toy_project/setup.sh /tmp/repoprover-toy-test
python -m repoprover run /tmp/repoprover-toy-test --pool-size 2 --verbose
```

Trajectory viewer:

```powershell
& ".\.venv-agents\Scripts\python.exe" -m repoprover.viewer --dir C:\path\to\lean\project\runs --port 8080
```

## LeanDojo

Installed from:

```text
external\LeanDojo
```

Use the Python 3.11 GPU environment:

```powershell
$LEAN_GPU = "C:\Users\Anwender\AppData\Local\anaconda3\envs\pytorch-gpu"
& "$LEAN_GPU\python.exe" -c "import lean_dojo, torch; print('lean_dojo ok'); print(torch.__version__); print(torch.cuda.is_available())"
```

Verified:

```text
lean-dojo==4.20.0
torch==2.9.1+cu128
cuda_available=True
```

LeanDojo README requirements:

- Linux, Windows WSL, or macOS
- Git >= 2.25
- Python `>=3.9,<3.13`
- `wget`
- `elan`
- `GITHUB_ACCESS_TOKEN`

On this native Windows shell, Python/torch/import works, `git` and `lake` are available, but `wget` and `GITHUB_ACCESS_TOKEN` are missing. For full LeanDojo repo tracing, prefer WSL or install `wget` and set `GITHUB_ACCESS_TOKEN`.

Useful local checks:

```powershell
& "$LEAN_GPU\python.exe" -m pip check
& "$LEAN_GPU\python.exe" -c "import importlib.metadata as m; print(m.version('lean-dojo'))"
```

LeanDojo examples are notebooks under:

```text
external\LeanDojo\scripts\demo-lean4.ipynb
external\LeanDojo\scripts\generate-benchmark-lean4.ipynb
```

## PDA

Installed from:

```text
external\PDA
```

Dependencies from `requirements.txt` were installed into `.venv-agents`.

Important README note: the released repo includes the FormL4 dataset and annotation assets, but says the training/evaluation code and finetuned autoformalizer/verifier will be released later. So locally, use it as:

- dataset source: `external\PDA\data\FormL4`
- prompt/reference source: `external\PDA\prompt`
- process-level architecture reference for compiler feedback and verifier loops

Quick dataset check:

```powershell
Get-ChildItem C:\Users\Anwender\Science-Work-Flow-\external\PDA\data\FormL4
```

## JFC

Installed from:

```text
external\jfc
```

The editable Python package installed as:

```text
slopspec==0.1.0
```

JFC's README expects:

- `pixi`
- Claude Code
- local data and an analysis config

Current machine check:

- `pixi` was not found on PATH.
- `claude` was not found on PATH.

Once those are installed, the README quick start is:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-\external\jfc
pixi run scaffold analyses\my_analysis --type measurement
cd analyses\my_analysis
# Edit .analysis_config: set data_dir and allowed paths.
pixi install
claude
```

## Lean REPL

Cloned at:

```text
external\lean-repl
```

This is a Lake/Lean project, not a Python package. It pins:

```text
leanprover/lean4:v4.30.0-rc2
```

Build command when ready:

```powershell
cd C:\Users\Anwender\Science-Work-Flow-\external\lean-repl
lake build
```

I did not build it in this pass.

## Reference But Not Locally Runnable Yet

`mephisto` is described as a central multi-agent astronomy framework in the local paper `references\resource\2409.14807v2.pdf`, but the paper extraction and Microsoft Research page do not expose a public GitHub code repository. Track it as paper-described, not installable.

Agent Laboratory has a public repository and is cited as related work, but it is not one of the central local papers installed in this pass. Add it as a second-scope install if you want all related-work agents too.
