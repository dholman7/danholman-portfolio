# AI Testing

AI-powered test generation and test data workflows.

- Stack: Python/TypeScript + LLM APIs
- Highlights: Prompt strategies, safety checks, reproducibility
- Paths:
  - `scripts/` – CLI scripts / notebooks

## Public vs Private Content

- Public configs live in `ai-testing/agents` and `ai-testing/prompts`.
- Private originals live in `ai-private/agents` and `ai-private/prompts` (private submodule recommended).
- Use `make redacted` from `ai-testing/` to generate sanitized artifacts from `ai-private/`.

### Private submodule setup (manual)

1. Create a private repo (e.g., `github.com/<org>/ai-private`).
2. Add it as a submodule mounted at `ai-private/`:
   - Run manually: `git submodule add <ssh-url> ai-private` (do not commit to public if not desired).
3. Keep `.env` and secrets inside `ai-private/` only.
4. Optional: set `AI_PRIVATE_ROOT` env var for scripts to reference.

## Detailed Guide: AI Testing Module

### Structure
- `agents/` – agent definitions (public-safe).
- `prompts/` – prompts safe for public.
- `evals/` – cases, scorers, and reports.
- `scripts/` – utilities (e.g., `redact.py`).
- `redacted/` – generated sanitized artifacts (gitignored).

### Agent rules explained
- Define models, capabilities (tools, browsing), and rules (tone, safety, SOPs).
- Public files show capabilities without sensitive SOPs or endpoints.
- Private files include full procedures and connectors.

### Using code and documents as context
- Add files under `evals/` or pass paths to your runner.
- The runner loads file contents and includes them in the prompt.
- Example case references `evals/example-cf.yaml`; replace with your own files.

### Workflows
- Redact from private: `make redacted`
- Run eval: `make eval-run`
- Lint/format: `make lint`, `make fmt`

### Environment
- Copy `.env.example` to `.env`.
- Set `OPENAI_API_KEY` and `MODEL_NAME` as needed.

### Private submodule
- Recommended to mount a private repo at `ai-private/` (ignored).
- Keep original prompts/agents/datasets there.



### Agent rules: where and how to demo in Cursor

- Public agent rules: `ai-testing/agents/` (e.g., `ai-testing/agents/example-agent.public.yaml`)
- Private/full rules: `ai-private/agents/` (ignored) (e.g., `ai-private/agents/example-agent.private.yaml`)

To demo in Cursor:
- Open `ai-testing/agents/example-agent.public.yaml` and ask Cursor to “explain and apply these rules to generate a new eval case” or “propose a redacted version of a private agent.”
- See `docs/cursor-demo.md` for suggested prompts and flow.
