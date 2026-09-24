# Security Policy

## Supported versions

Only the latest release on `main` receives security fixes.

## Reporting a vulnerability

Report privately via GitHub Security Advisories (Security tab → *Report a
vulnerability*), or through your internal security contact. Do not open a
public issue with exploit details. Expect an acknowledgement within a few
business days.

## Security model and trust boundaries

Dev is a local, on-device decision engine. The boundaries you must treat as
security-relevant:

1. **Model files are code.** `dev.load(...)` and `Router` download a checkpoint
   from the Hugging Face Hub and build an arbitrary network architecture from
   its config and weights, then execute it. Only load checkpoints you trust
   (the official `convaiinnovations/laya*` repos, or ones your own team
   produced). The runtime loads weights through **safetensors only** — pickled
   checkpoints are rejected, and subfolder paths cannot traverse outside the
   model directory.
2. **The HTTP server (`dev-serve`)** binds `127.0.0.1` by default. Binding a
   non-loopback address without `DEV_API_KEY` prints a warning; for any remote
   exposure set `DEV_API_KEY` (constant-time bearer check) and terminate TLS at
   a reverse proxy. Request bodies are capped (2 MiB, 64 questions, 50k-char
   state) and inference errors are not leaked to clients.
3. **The MCP server (`dev-mcp-server`)** runs over stdio. Internal error
   details are logged locally and redacted from tool results, which an LLM may
   incorporate into prompts.
4. **No telemetry.** Dev sends nothing anywhere except the model downloads you
   explicitly request from the Hub.
5. **Dependencies.** CI runs pip-audit (CVE audit), CodeQL, gitleaks secret
   scanning, and Dependabot (weekly). Keep the `security` workflow green.
6. **Decision output is model output, not code.** Question instructions and
   state text are model inputs; Dev never executes them. Callers should treat
   answers as untrusted data — gating on calibrated confidence is still a
   probability, not a proof.

## Hardening changes vs upstream laya

- `dev-serve` defaults to loopback and warns on unauthenticated non-loopback
  bindings (upstream defaulted to `0.0.0.0` with no auth requirement).
- MCP internal-error details are redacted from client responses.
- Model subfolder resolution refuses `..`/absolute paths (Python + TypeScript).
- TypeScript SDK: HTTPS-only model fetches, download size caps, thread-count
  clamp, `NaN` LRU-cap fix, reserved-key rejection (`__proto__` defense).
- Language detection caps regex input; BPE chunking bounds quadratic work.
- ONNX export helper loads checkpoints with `weights_only=True` (no pickle).
- CI actions pinned to commit SHAs where practical.
