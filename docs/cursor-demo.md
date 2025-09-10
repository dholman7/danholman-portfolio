# Cursor Demo: Repo-Wide AI Assistance

> Cursor is an AI code editor built to make you extraordinarily productive, with repo-wide code understanding, natural language editing, and powerful autocompletion. Learn more at https://cursor.com/.


This guide shows how to use Cursor to leverage full-repo context beyond typical chat responses.

## Why Cursor here?
- Repo-aware suggestions: understands `automation-framework/`, `cloud-native-app/`, and `ai-test-generation/` at once.
- Tooling integration: read/write files, run commands, and propose structured edits.
- Safer workflows: can be constrained to only modify targeted files and show diffs.

## Suggested demo flow (mock-only)

1) Navigate and index
- Open the repo in Cursor; let it index the project.
- Ask: "Give me a summary of the repo structure and the purpose of each module."

2) Cross-referencing docs and code
- Ask: "Using `ai-test-generation/evals/cases/summarize.jsonl` and `ai-test-generation/evals/example-cf.yaml`, explain how the eval case uses the context file."

3) Add a small feature with edits
- Prompt: "Add a new eval case that checks for the presence of Outputs in a template; name it `outputs.jsonl`."
- Review the proposed edits (Cursor shows diffs), accept or refine.

4) Repo-wide refactor (scoped)
- Prompt: "In `automation-framework/`, add an ESLint config and wire it in the Makefile lint target. Avoid changing other modules."

5) Safety and redaction
- Prompt: "Add a pre-commit message to the README warning not to commit secrets; confirm `.gitignore` excludes `ai-private/` and `.env` files."

## Best practices
- Be explicit about file paths and constraints in prompts.
- Use "show me the diff before applying" to review changes.
- Keep mock-only by not providing real API keys; keep everything in `.env.example`.
- For larger changes, ask Cursor to create TODOs and proceed step-by-step.

## What to highlight live
- Cursor finds related files quickly (e.g., connects Makefile targets with scripts).
- It can read `README.md` + `docs/` + code together to maintain consistency.
- It respects `.gitignore` and won’t accidentally include `ai-private/` if configured.
