# feature-map

A skill for Claude Code (and other agents that read `SKILL.md`) that has an agent reproduce, verify and harden code changes, instead of guessing at a fix:

- **Closed-loop verification:** reproduce in the real app, make a small fix, re-run the same check, and report before/after evidence.
- **`FEATURE_MAP.md`:** a map of each feature's code, how to reach it, and its selectors. It is created only for projects with a UI or more than 15 source files.
- **Guardrails:** turn a mistake agents keep making into a lint rule or CI check.
- **Eval loop:** score the skill with blind runs by subagents.

The skill is written in Spanish and is based on the Pstack/Dune architecture by Lauren Tan.

## Install

```bash
git clone https://github.com/nicoliniyo/feature-map.git
mkdir -p ~/.claude/skills
cp -r feature-map/skills/feature-map ~/.claude/skills/
```

In Claude Code, invoke it with `/feature-map`, or let Claude load it automatically when its description matches the task.

## Works with

- **[spec-driven-development](https://skills.sh/addyosmani/agent-skills/spec-driven-development)**: the spec and its approval gates decide what to build; this skill verifies each task in the real app, using `FEATURE_MAP.md` for the route and selectors.
- **[anchored-decisions](https://github.com/nicoliniyo/anchored-decisions)**: records why a feature is built the way it is. Its `anchor-check` CLI also checks `FEATURE_MAP.md`, reporting entries whose code location or `data-testid`/`aria-label` selectors no longer exist.

The skill's "Integración con spec-driven-development y anchored-decisions" section explains how they fit together. It applies only when the project already uses one of them.

## Evaluation

The skill was tested in two rounds of paired subagent runs, each task done once with the skill and once without:

- **Round 1:** a bug and a performance fix.
- **Round 2:** a UI bug, a 33-file repo with a decoy fix, and a "don't test it" pressure task.

Every agent fixed its task, with or without the skill. The skill made the evidence somewhat more thorough and produced a useful `FEATURE_MAP.md` where one was called for. It did not change whether agents found the right fix.

The scenarios, prompts and graders are in [`evals/`](evals/).

## License

[MIT](LICENSE)
