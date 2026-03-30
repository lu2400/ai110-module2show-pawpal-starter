# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The `Scheduler` class has two extra features:

- **Recurring tasks** — marking a daily or weekly task complete automatically adds the next one to the pet's list. Daily tasks are always due tomorrow; weekly tasks are due 7 days later.

- **Conflict detection** — `find_conflicts()` checks whether any two tasks are scheduled at the same time. If conflicts are found, a warning is printed so the owner can fix the schedule before it causes problems.

## Testing PawPal+

### Run the tests

```bash
python -m pytest test/test_pawpal.py -v
```

### What the tests cover

| Area | What is verified |
| --- | --- |
| **Sorting** | Tasks are returned in chronological order; a dedicated test also documents the known string-sort bug at the 9→10 AM boundary |
| **Recurring tasks** | Daily tasks get a new due date of today + 1 day; weekly tasks advance by 7 days from the original date; the new task is added to the correct pet; one-off tasks do not recur |
| **Conflict detection** | Flags two tasks at the same time on the same pet or across different pets; confirms no false positives for different times or a single task |
| **Scheduling** | Respects `max_minutes`; zero budget returns empty; priority tasks are scheduled first; overworked owners are capped at half their available time |
| **Edge cases** | Pet with no pending tasks, owner with no pets |

### Confidence level

⭐⭐⭐⭐ (4/5)

The core scheduling logic, recurrence rules, and conflict detection are all covered and passing (21/21). One star is withheld because `sort_by_time` has a known string-sort bug at the 9→10 AM boundary that is documented but not yet fixed, and task duration is hardcoded at 30 minutes rather than derived from real task data.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
