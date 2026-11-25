---
name: feature-map
description: Use when fixing bugs, optimizing performance or implementing features where the change must be proven by running the real app (reproduce before, verify after with evidence), when receiving vague reports ("it's slow", screenshots without context), when creating or maintaining a FEATURE_MAP.md, or when turning recurring agent mistakes into hard guardrails (linters, CI checks). Closed-loop verification based on Lauren Tan's Pstack/Dune architecture.
---

# Agent Verification Loop & Guardrails

This skill turns the agent from a speculative code generator into an autonomous engineer able to **reproduce, verify, prove and harden** changes to the codebase without constant human intervention (so the user is not the bottleneck).

---

## Core Principles

1. **Zero guessing (Read Before Hypothesizing):** Never state the root cause of a problem without first reading the exact files involved and tracing the real execution flow.
2. **The shortest path must be the best path:** Code structure and selectors must be documented so that navigating to and changing a feature is deterministic.
3. **Closed-loop verification:** A change is not done when it compiles; it is done when the agent runs the real application (as a user would), reproduces the scenario and captures objective before-and-after evidence.
4. **Progressive hardening:** Markdown instructions are *soft constraints* (the agent can forget them). Every recurring error pattern must become a *hard constraint* (a linter rule, a dependency check or a CI check).

---

## Workflow 1: Creating and Maintaining `FEATURE_MAP.md`

Look for `FEATURE_MAP.md` in the project root or in `.agent/` and apply the first rule that matches:

| Observable situation | Action |
|---|---|
| `FEATURE_MAP.md` exists | Consult it in Phase 1 and update the entries your change affects. |
| It does not exist **and** the project has a user interface (web, mobile, desktop, TUI) | Create it before Phase 2, with at least the entry for the feature you are touching. |
| It does not exist **and** the project has more than 15 source files | Create it before Phase 2, with at least the entry for the feature you are touching. |
| None of the above | Do not create it. In the Closing Report write: "FEATURE_MAP.md skipped: project has no UI and ≤15 source files." |

Structure of each entry:

```markdown
# Feature Map

## [Feature / View Name]
- **Code location:** `path/to/co-located/directory/`
- **Navigation path (user):** Step 1 -> Step 2 -> Action
- **Keyboard shortcuts / commands:** `Cmd+K` / `npm run dev`
- **Deterministic selectors (CDP / Playwright / Maestro):**
  - Main container: `[data-testid="..."]`
  - Triggering action: `button[aria-label="..."]`
- **Process / execution thread:** Main thread / Renderer / Server Action / Worker
- **Critical invariants:** (e.g. "Must not block the render thread > 16ms", "Do not import server modules in the client")
```

### Map maintenance rules:
- Whenever you create a new feature or change routes/selectors, update the matching entry in `FEATURE_MAP.md` in the same PR or change set.
- Keep all code related to a feature co-located in a single directory whenever the architecture allows it.

---

## Workflow 2: Closed-Loop Verification Protocol

For any bug fix, performance optimization or new feature, follow these 5 phases strictly:

### Phase 1: Triage and Real Localization
1. Consult `FEATURE_MAP.md` to identify the exact location of the feature.
2. Read the relevant source files and their direct dependencies.
3. If the report is ambiguous (e.g. a screenshot or a vague description), cross-check the visual elements against the map's selectors before forming a hypothesis.

### Phase 2: Reproduction in a Real Environment
Start the application locally in development or test mode, using the native tool for the stack:
- **Web / Electron:** Chrome DevTools Protocol (CDP), Playwright or Puppeteer (capturing console logs, network errors, performance/CPU traces and *heap snapshots*).
- **Mobile (iOS / Android / Flutter):** Native simulators (`xcrun simctl`, `adb`, `flutter test` / integration) capturing state and frame metrics.
- **Backend / CLI:** Run the binary directly, hit real endpoints, or run integration suites against an isolated environment.

*Requirement:* Capture evidence of the initial state (**Before**) that demonstrates the failure or the current behavior.

### Phase 3: Atomic Implementation
1. Make small, focused changes that are easy to revert.
2. Avoid unnecessary historical or narrative comments in the code; the code should explain itself and the Git history should describe why the commit was made.
3. Strictly respect layer isolation (e.g. do not mix heavy I/O logic into the UI render thread).

### Phase 4: Evidence Verification (After)
1. Re-run exactly the same reproduction flow from Phase 2.
2. Compare metrics and behavior (**Before vs. After**):
   - Did the console errors/exceptions go away?
   - Is the performance budget kept (e.g. < 16ms per frame for 60fps)?
   - Did adjacent features stay intact?
3. If verification fails, **do not deliver the code**. Analyze the real trace, adjust and iterate until the test passes deterministically.

### When the environment blocks execution (Phases 2 and 4)
"Verification fails" means the test ran and gave a wrong result. If the test **cannot be run** (permission denied, a server that will not start, the `file://` protocol blocked, a missing simulator), go through this table in order: the first row always applies if there was a denial, and of the others use the first one you can carry out.

| Observable situation | Action |
|---|---|
| A permission was denied (the tool responded with a denial from the user or the permission mode) | Do not retry that action by another route (a script, another tool, foreground instead of background): the denial is the user's decision. Move on to the following rows only with routes that do not do what was denied. |
| A technical failure (port in use, `file://` blocked, a process that will not start) and a time-limited alternative route exists (e.g. another port, a script that starts the server, runs Playwright/CDP headless and stops it, with `timeout 60`) | Use it for reproduction and verification. Record in the report which alternative route you used. |
| A test exists that is closer to the user than reading the code and does not need what was denied (an integration test, running the binary, `elementFromPoint` in a DOM loaded by a script) | Run it before and after the change. Write **PARTIAL VERIFICATION** on the first line of the report, list what the test did not cover (e.g. the real server, other views, real storage) and give the concrete steps for full verification. If the cause was a permission, name the permission that would need to be granted. |
| No execution route works | Deliver the change marked **UNVERIFIED**: write that word on the first line of the report, say which route failed and with what exact error, and give the concrete steps (command, URL, selector, expected result before and after) for the user to verify. If the cause was a permission, name the permission that would need to be granted. |

### Phase 5: Closing Report
Give the user a concise summary that includes:
- The verified root cause (with a file and line reference).
- Evidence of the initial reproduction vs. the final verification, or the **PARTIAL VERIFICATION** / **UNVERIFIED** marker with the pending verification steps.
- `FEATURE_MAP.md`: entries created or updated, or the skip line from Workflow 1.

---

## Workflow 3: From Recurring Error to Hard Constraint (Guardrails)

When you notice that an agent (you or a subagent) makes a structural mistake or breaks a project convention:

1. **Identify the pattern:** Is it an architecture problem (e.g. importing forbidden modules across folders), a framework anti-pattern (e.g. uncontrolled side effects) or a performance regression?
2. **Propose or implement a hard constraint:**
   - A custom rule in ESLint / Biome / Analyzer / Clippy.
   - A dependency-graph check in the CI pipeline.
   - Strict typing that makes invalid states impossible to represent.
3. **Goal:** The build or CI fails automatically if the pattern is reintroduced, removing the need for human review of that problem.

---

## Integration with spec-driven-development and anchored-decisions

Apply this section only if the project already uses one of these skills: there is a `spec/SPEC.md` or `tasks/todo.md` (spec-driven-development), or a `DECISIONS.md` (anchored-decisions). If there is neither, ignore it.

Each skill answers a different question; do not copy one's content into another:

| Skill | Question | File |
|---|---|---|
| spec-driven-development | What are we building, and when is it done? | `spec/SPEC.md`, `tasks/` |
| feature-map | Where does the feature live, how do you reach it, and did the change work? | `FEATURE_MAP.md` |
| anchored-decisions | Why is it built this way, and is that still true? | `DECISIONS.md` |

- **Approvals belong to the spec; autonomy belongs to implementation.** spec-driven-development's human approval gates apply to the spec and the plan. This skill's five phases run without waiting for approval inside each already-approved task.
- **Each task's `Verify:` uses the map.** When a task in `tasks/todo.md` touches a feature that has an entry in `FEATURE_MAP.md`, its verification is that entry's navigation path and selectors (Phases 2 and 4).
- **Project structure lives in one place.** The spec's "Project Structure" section describes only the top-level layout; each feature's location lives in the map.
- **Critical invariants are decisions.** If an invariant in a map entry must not be re-argued, record it as a `D-xx` in `DECISIONS.md` (with anchors and a `Why not`) and link its id from the invariant line.
- **Guardrails are anchors.** A linter or CI rule created in Workflow 3 is a strong anchor for its decision (e.g. `config: .eslintrc.json#no-restricted-imports`).
- **The verification level goes into `Verified:`.** Full before/after verification → `Verified: <date> (local)` (or the environment used). **PARTIAL VERIFICATION** → `(code-only)`. **UNVERIFIED** → the record stays `PROPOSED`.
- **Close in the same commit.** Update the map entry, update `Verified:` on the affected decisions (or supersede them with a new record) and set planned decisions to `ACTIVE`.
- **The map is checked too.** If `anchor-check` is available, run it before the Closing Report: it verifies that each entry's location exists and that each `[attr="value"]` selector still appears in the code. Fix any `BROK` on an entry your change touched and mention it in the report.

---

## Workflow 4: Skill Self-Evaluation (Eval Loop)

When you change this skill or set up verification for a new repository, validate its effectiveness in isolation:

1. **Define an objective rubric (0 to 10):**
   - *Localization:* Did it find the right code without exploring irrelevant files?
   - *Reproduction:* Did it run the real app before editing code?
   - *Precision:* Did it fix the root cause without introducing side effects?
   - *Evidence:* Did it deliver verifiable proof of the result?
2. **Blind test with subagents:** Run test tasks in isolated directories or *worktrees* with neutral names (without signalling in the environment that it is an evaluation, to avoid behavioral bias).
3. **Cross-audit:** Review the subagent's tool calls and reasoning blocks to find where it hesitated or guessed, and refine `FEATURE_MAP.md` or the verification scripts until it scores consistently.
