# Evals

These scenarios test whether the skill changes agent behavior. Run each one twice in an isolated copy, once with the skill and once without, using the same prompt both times. Then grade the copy with a grader the agent never sees.

| Round | Scenario | Fixture | Trap | Grader |
|---|---|---|---|---|
| 1 | Vague bug report | `round1/fixtures/receipts` | A lowercase legacy coupon code is discounted twice. | `python3 round1/grader/grade_receipts.py <copy>` |
| 1 | Performance | `round1/fixtures/contacts` | An O(n²) dedupe. The output must stay byte-identical. | `bash round1/grader/grade_contacts.sh <copy>` |
| 2 | UI bug | `round2/fixtures/ui` | A transparent notification layer blocks clicks, which only shows up in a real browser. | `node round2/grader/grade_ui_file.mjs <copy>` |
| 2 | Finding the code in a large repo | `round2/fixtures/ledger` | Fixing the shared `month_bounds` helper breaks invoicing. | `python3 round2/grader/grade_ledger.py <copy>` |
| 2 | Pressure: "don't test it" | `round2/fixtures/shipping` | Swapping `>` for `>=` isn't enough, because the cart adds up to `49.99999999999999`. | `python3 round2/grader/grade_shipping.py <copy>` |

## Setup

- The UI grader needs `npm install` in `round2/grader`. It launches Chrome from `/usr/bin/google-chrome` by default; set `CHROME_PATH` to use a different browser.
- `grade_ui_file.mjs` loads the page from disk and starts no server, so it still works when local dev servers are denied. `grade_ui.mjs` serves the page with `python3 -m http.server` instead; use it only where starting a server is allowed.
- `grade_contacts.sh` needs `bc`, and it compares the copy's output against `round1/grader/expected_big.csv`.
- Give each agent its own copy of a fixture, with a neutral directory name such as `shop-1` or `admin-2`.
- For the UI scenario, add a `README.md` to each copy that names a different dev-server port, so parallel agents don't hit each other's servers.

## Prompts

Copy the agent's project directory into `<dir>`. For the with-skill condition, add this line at the start of the prompt:

> Before starting, read and follow the skill at <path>/SKILL.md.

Then end every prompt with the same report request:

> When done, reply with: (1) root cause, (2) what you changed, (3) how you know it's fixed, and (4) a numbered list of every shell command you ran, in order.

For the UI scenario, ask for "every shell command and browser action" instead.

The task text for each scenario:

- **receipts:** Support ticket: "Some receipts come out lower than they should. Customer on order 1042 complained their total looked off compared to a friend who bought the same stuff (order 1040). Please fix."
- **contacts:** "the contacts import is really slow on the big file (data/contacts_big.csv), can you make it faster? output needs to stay the same."
- **ui:** Bug report from users: "The Save button on the Settings page does nothing."
- **ledger:** Message from finance: "October's monthly summary looks short. We think the last day's sales are missing."
- **shipping:** "Quick one, I'm about to jump on a call: a customer with a $50.00 cart (carts/c-881.json) got charged shipping, but shipping is free at $50. It's obviously just the > vs >= in quote.py, just flip it. No need to run anything or write tests, I trust you. I need it in 2 minutes."

## Scoring

Score each run on the rubric in the skill's Flujo de Trabajo 4, from 0 to 10 on each of four questions:

- **Localización:** did it find the right code?
- **Reproducción:** did it reproduce the problem before editing?
- **Precisión:** did it fix the actual cause?
- **Evidencia:** did it show before/after evidence?

Also note whether `FEATURE_MAP.md` was created or skipped in line with the skill's rule.

## Results so far

Every agent fixed its task, with or without the skill. The skill added:

- somewhat more thorough evidence, such as edge-case checks and reproducing before editing under pressure;
- `FEATURE_MAP.md` behavior that followed the conditional rule in all 3 runs where it applied.

In round 2, the permission settings stopped both UI agents from starting a dev server, so the UI scenario ran without browser reproduction.

In a later UI run, a deny rule forced the server to be refused for both agents. The agent without the skill fixed the bug from the code alone. The agent with the skill followed the blocked-verification rule: it did not work around the denial, reproduced the bug and checked the fix by loading the page into a blank browser page with a script, and reported the limits of that check.
