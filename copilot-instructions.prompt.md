---  
agent: ask  
description: A detailed GitHub-style prompt guiding code generation and review for Python projects. Includes structure, naming, error handling, security, testing, examples, and expectations.  
model: gpt-5-mini  
---

# Copilot / Assistant Prompt — Python Best Practices

Purpose
- Provide a canonical set of instructions for generating, reviewing, and editing Python code in this repository.
- Ensure code follows modern standards for readability, security, testability, and maintainability.

Tone & Constraints
- Be concise, pragmatic, and risk-aware.
- Prefer small, focused changes; do not refactor unrelated code without explicit approval.
- Explain non-trivial trade-offs in one sentence plus a one-paragraph rationale.
- Avoid leaking secrets or suggesting insecure defaults.

How to use
- Paste this entire file into your GitHub prompt.md (or VS Code Copilot prompt) area.
- When asked to edit code, produce an apply_patch-style diff or a minimal code block plus tests.
- Include a one-line commit message and one-paragraph justification when proposing repository edits.

Core principles
- Readability: prefer explicit, idiomatic Python.
- Correctness: validate inputs, fail fast on misuse.
- Minimalism: smallest change that fixes the issue.
- Testability: code should be easy to unit test.

Style & Tooling
- Follow PEP 8. Use 4-space indentation.
- Format with `black`; lint with `ruff`/`flake8`.
- Use `mypy`/`pyright` in CI; add type hints for public APIs.
- Add pre-commit hooks for `black`, `ruff`, and `mypy` checks where applicable.

Repository structure (recommended)
- my_package/
  - __init__.py
  - cli.py
  - core.py
  - utils.py
  - _internal.py
- tests/
  - test_core.py

Naming conventions
- Modules/packages: short_lowercase (e.g., `utils.py`)
- Functions/variables: lower_snake_case
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Private names: single_leading_underscore

Code structure recommendations
- Small modules with clear responsibility.
- Keep public API surface minimal; use `__all__` where helpful.
- Prefer pure functions for logic; isolate I/O.

Examples

1) Clear, typed function with docstring and validation
```python
from typing import List

def compute_mean(values: List[float]) -> float:
    """Return the arithmetic mean of a non-empty list of floats.

    Args:
        values: A non-empty list of floats.

    Returns:
        The arithmetic mean.

    Raises:
        ValueError: if `values` is empty.
    """
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)
```

2) Specific exception handling with logging and exception chaining
```python
import json
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def load_config(path: str) -> Dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        logger.error("Config file not found: %s", path)
        raise
    except json.JSONDecodeError as exc:
        logger.exception("Invalid JSON in config: %s", path)
        raise ValueError("invalid config file") from exc
```

3) Avoid mutable defaults
```python
from typing import Optional, List

def append_unique(items: Optional[List[int]] = None) -> List[int]:
    if items is None:
        items = []
    items.append(1)
    return items
```

Security best practices
- Never hard-code credentials or secrets. Use environment variables or secret stores.
- For subprocesses, avoid `shell=True`. Use `subprocess.run([...])` with an argument list.
- For SQL, always use parameterized queries or an ORM.
- Validate and sanitize external inputs; never use `eval` on untrusted data.

Security examples
```python
import os

DB_PASSWORD = os.getenv("DB_PASSWORD")
if not DB_PASSWORD:
    raise RuntimeError("DB_PASSWORD must be set in environment")
```

```python
import sqlite3

def get_user_by_email(conn: sqlite3.Connection, email: str):
    cur = conn.execute("SELECT id, email FROM users WHERE email = ?", (email,))
    return cur.fetchone()
```

Testing
- Use `pytest` for unit tests.
- Keep tests fast and deterministic; mock I/O and network calls.
- Include at least one happy-path test and one edge-case/failure test for new functionality.

Example tests (tests/test_core.py)
```python
from my_package.core import compute_mean
import pytest

def test_compute_mean_basic():
    assert compute_mean([1.0, 2.0, 3.0]) == 2.0

def test_compute_mean_empty():
    with pytest.raises(ValueError):
        compute_mean([])
```

Error handling & logging
- Catch specific exceptions, not bare `except:`.
- Use `raise ... from ...` to preserve exception context when wrapping.
- Use structured logging with appropriate levels; do not print in libraries.

Type hints & static analysis
- Annotate public functions and classes.
- Run `mypy`/`pyright` in CI; fix errors introduced by changes.
- Use `TypedDict`, `Protocol`, and `Final` where they make interfaces clearer.

Packaging & dependencies
- Prefer standard library when sufficient.
- Pin direct dependencies and use a lockfile for reproducible installs (`poetry.lock` or pinned `requirements.txt`).
- Document reasoning for adding any dependency.

Commit & patch guidance
- Produce focused diffs; explain intent in the commit message.
- Commit message example:
  - Title: "Fix: validate empty input in compute_mean()"
  - Body: "Raise ValueError when `values` is empty to prevent ZeroDivisionError. Adds two unit tests. No public API changes."

Deliverables when editing code
- Minimal apply_patch-style diff or file contents.
- Updated/added tests exercising behavior.
- One-line summary and one-paragraph rationale for the change.
- Commands to run tests locally (example):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Quick checklist for PRs
- [ ] Small, focused changes
- [ ] Type hints for public API
- [ ] Docstrings (Google/NumPy style)
- [ ] Tests added/updated
- [ ] Linter (`ruff`/`flake8`) and formatter (`black`) pass
- [ ] CI: static type checks pass

Appendix — common patterns & anti-patterns
- Prefer f-strings: `f"count={n}"` over `%` or `.format`.
- Avoid deeply nested code; extract helpers.
- Do not swallow exceptions silently.
- Avoid mutable default args.

End of prompt
