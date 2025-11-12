# AGENTS.md (repo-wide)

- Scope: applies to the whole repo (frontend in `desi-jarvis/` and Python agent in repo root).
- Frontend install/dev/build: `cd desi-jarvis && pnpm install && pnpm dev` • build: `pnpm build`.
- Lint/format (frontend): `pnpm lint` • format write: `pnpm format` • check: `pnpm format:check`.
- Tests (frontend): none configured. If you add Vitest/Jest, run a single test with e.g. `pnpm vitest -t "name"`.
- Python (root) install/run: `uv sync` • run agent: `uv run python agent.py`.
- Tests (python): none configured. If you add pytest, run a single test with `uv run pytest -k "expr"`.
- ESLint (frontend): extends `next/core-web-vitals`, `next/typescript`, `plugin:import/recommended`, `prettier` (see `desi-jarvis/eslint.config.mjs`, `.eslintrc.json`).
- Prettier (frontend): enforced in CI; key settings: `singleQuote: true`, `semi: true`, `trailingComma: es5`, `printWidth: 100`, `tabWidth: 2` (`desi-jarvis/.prettierrc`).
- Import order (frontend): `react`, `next`, `next/*`, third‑party, `@*`, `@/*`, then relative; specifiers sorted; handled by `@trivago/prettier-plugin-sort-imports`.
- Tailwind: class order auto-sorted via `prettier-plugin-tailwindcss`.
- TS config: `strict: true`, path alias `@/*` (prefer absolute over deep relative); no `any`; use `import type` for type-only imports.
- Naming: React components PascalCase; hooks camelCase starting with `use...`; files generally kebab-case (e.g., `agent-control-bar.tsx`).
- Error handling (API routes): validate required env early; use `try/catch`; log with `console.error`; return `NextResponse.json(..., { status })`; avoid leaking secrets.
- Error handling (UI): surface errors via callbacks/toasts; keep error objects serializable across boundaries; don’t silently swallow.
- Python style: modules/functions snake_case; raise explicit exceptions; do not log secrets; keep side effects in `if __name__ == "__main__":` when applicable.
- CI (GitHub Actions): runs `pnpm install`, `pnpm lint`, `pnpm format:check`, `pnpm build` on Node 22 (see `desi-jarvis/.github/workflows/build-and-test.yaml`).
- Cursor/Copilot: no repository-specific Cursor rules or Copilot instructions found.
- General rule: match existing patterns in `desi-jarvis/` and keep changes minimal and consistent.
