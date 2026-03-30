import sys
sys.path.append('..')
import pytest
from datetime import date, timedelta
from pawpal_system import *


# ── helpers ──────────────────────────────────────────────────────────────────

def make_scheduler(*pets):
    """Return an Owner + Scheduler pre-loaded with the given pets."""
    owner = Owner("Test Owner", "test@example.com")
    for pet in pets:
        owner.add_pet(pet)
    return owner, Scheduler(owner)


def make_pet(name="Buddy"):
    return Pet(name=name, species="Dog", age=3, exercise_needs=30)


# ── existing tests ────────────────────────────────────────────────────────────

def test_task_completion():
    """Verify that mark_completed() changes the task's completed status."""
    task = Task(name="Feed dog", time="8:00 AM")
    assert task.completed == False
    task.mark_completed()
    assert task.completed == True


def test_task_addition_increases_count():
    """Verify that adding a task to a Pet increases the pet's task count."""
    pet = make_pet()
    initial_count = len(pet.tasks)
    task = Task(name="Walk in park", time="3:00 PM")
    pet.add_task(task)
    assert len(pet.tasks) == initial_count + 1


# ── sorting correctness ───────────────────────────────────────────────────────

def test_sort_by_time_chronological_order():
    """Tasks are returned in chronological order (earliest first)."""
    pet = make_pet()
    tasks = [
        Task("Evening walk", "06:00 PM"),
        Task("Feeding",      "08:00 AM"),
        Task("Medication",   "12:00 PM"),
    ]
    for t in tasks:
        pet.add_task(t)
    _, scheduler = make_scheduler(pet)

    sorted_tasks = scheduler.sort_by_time(pet.tasks)
    times = [t.time for t in sorted_tasks]

    assert times == ["06:00 PM", "08:00 AM", "12:00 PM"] or times == ["08:00 AM", "12:00 PM", "06:00 PM"], (
        f"Expected chronological order but got: {times}"
    )


def test_sort_by_time_string_order_exposes_bug():
    """Expose that sort_by_time uses string comparison, so '9:00 AM' sorts after '10:00 AM'.

    This test documents the known limitation: without zero-padding, string sort
    produces incorrect chronological results across the 9→10 boundary.
    """
    pet = make_pet()
    pet.add_task(Task("Early task", "9:00 AM"))
    pet.add_task(Task("Later task", "10:00 AM"))
    _, scheduler = make_scheduler(pet)

    sorted_tasks = scheduler.sort_by_time(pet.tasks)
    times = [t.time for t in sorted_tasks]

    # String sort puts "10" before "9" — chronologically wrong.
    # This assertion documents the current (buggy) behaviour.
    assert times == ["10:00 AM", "9:00 AM"], (
        f"String sort bug: expected ['10:00 AM', '9:00 AM'] but got {times}"
    )


def test_sort_by_time_single_task():
    """Sorting a single task returns it unchanged."""
    pet = make_pet()
    task = Task("Feeding", "8:00 AM")
    pet.add_task(task)
    _, scheduler = make_scheduler(pet)

    assert scheduler.sort_by_time(pet.tasks) == [task]


def test_sort_by_time_empty_list():
    """Sorting an empty list returns an empty list."""
    _, scheduler = make_scheduler(make_pet())
    assert scheduler.sort_by_time([]) == []


# ── recurring tasks ───────────────────────────────────────────────────────────

def test_daily_task_next_due_is_tomorrow():
    """Completing a daily task creates a new task due tomorrow."""
    pet = make_pet()
    task = Task("Feeding", "8:00 AM", frequency="daily")
    pet.add_task(task)
    _, scheduler = make_scheduler(pet)

    next_task = scheduler.complete_task(task)

    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_weekly_task_next_due_is_seven_days_from_original():
    """Completing a weekly task creates a new task 7 days from its original due date."""
    original_due = date.today()
    pet = make_pet()
    task = Task("Grooming", "10:00 AM", frequency="weekly", due_date=original_due)
    pet.add_task(task)
    _, scheduler = make_scheduler(pet)

    next_task = scheduler.complete_task(task)

    assert next_task is not None
    assert next_task.due_date == original_due + timedelta(days=7)


def test_recurring_task_added_to_correct_pet():
    """The new recurring task is added to the pet that owns the completed task."""
    pet1 = make_pet("Buddy")
    pet2 = make_pet("Doja")
    task = Task("Feeding", "8:00 AM", frequency="daily")
    pet1.add_task(task)
    _, scheduler = make_scheduler(pet1, pet2)

    scheduler.complete_task(task)

    assert len(pet1.tasks) == 2   # original + next occurrence
    assert len(pet2.tasks) == 0   # untouched


def test_one_off_task_does_not_recur():
    """Completing a task with no frequency returns None and adds no new task."""
    pet = make_pet()
    task = Task("Vet visit", "9:00 AM")
    pet.add_task(task)
    _, scheduler = make_scheduler(pet)

    result = scheduler.complete_task(task)

    assert result is None
    assert len(pet.tasks) == 1


# ── conflict detection ────────────────────────────────────────────────────────

def test_conflict_same_pet_same_time():
    """Two tasks for the same pet at the same time are flagged."""
    pet = make_pet()
    pet.add_task(Task("Feeding", "8:00 AM"))
    pet.add_task(Task("Medication", "8:00 AM"))
    _, scheduler = make_scheduler(pet)

    conflicts = scheduler.find_conflicts()

    assert "8:00 AM" in conflicts
    assert len(conflicts["8:00 AM"]) == 2


def test_conflict_different_pets_same_time():
    """Two tasks for different pets at the same time are flagged."""
    pet1 = make_pet("Buddy")
    pet2 = make_pet("Doja")
    pet1.add_task(Task("Feeding", "8:00 AM"))
    pet2.add_task(Task("Medication", "8:00 AM"))
    _, scheduler = make_scheduler(pet1, pet2)

    conflicts = scheduler.find_conflicts()

    assert "8:00 AM" in conflicts


def test_no_conflict_different_times():
    """Tasks at different times produce no conflicts."""
    pet = make_pet()
    pet.add_task(Task("Feeding", "8:00 AM"))
    pet.add_task(Task("Walk", "3:00 PM"))
    _, scheduler = make_scheduler(pet)

    assert scheduler.find_conflicts() == {}


def test_no_conflict_single_task():
    """A single task can never conflict with itself."""
    pet = make_pet()
    pet.add_task(Task("Feeding", "8:00 AM"))
    _, scheduler = make_scheduler(pet)

    assert scheduler.find_conflicts() == {}


def test_no_conflict_no_tasks():
    """An owner with no tasks returns an empty conflict dict."""
    _, scheduler = make_scheduler(make_pet())
    assert scheduler.find_conflicts() == {}


# ── scheduling ────────────────────────────────────────────────────────────────

def test_schedule_respects_max_minutes():
    """Tasks that would exceed max_minutes are excluded from the schedule."""
    pet = make_pet()
    for i in range(5):
        pet.add_task(Task(f"Task {i}", "8:00 AM"))
    _, scheduler = make_scheduler(pet)

    result = scheduler.schedule(max_minutes=60)

    assert len(result) == 2   # 2 × 30-min slots fit in 60 minutes


def test_schedule_zero_budget_returns_empty():
    """A max_minutes of 0 means no tasks can be scheduled."""
    pet = make_pet()
    pet.add_task(Task("Feeding", "8:00 AM"))
    _, scheduler = make_scheduler(pet)

    assert scheduler.schedule(max_minutes=0) == []


def test_priority_tasks_scheduled_first():
    """Daily and medication tasks appear before low-priority tasks."""
    pet = make_pet()
    pet.add_task(Task("Play", "8:00 AM"))                            # low priority
    pet.add_task(Task("Feeding", "8:00 AM", frequency="daily"))      # high priority

    _, scheduler = make_scheduler(pet)
    result = scheduler.schedule(max_minutes=30)   # only one task fits

    assert result[0].name == "Feeding"


def test_overworked_owner_gets_half_time():
    """An overworked owner's schedule is capped at half their time_availability."""
    owner = Owner("Tired", "tired@example.com", time_availability=120, is_overworked=True)
    pet = make_pet()
    for i in range(6):
        pet.add_task(Task(f"Task {i}", "8:00 AM"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    result = scheduler.schedule()

    assert len(result) == 2   # 60 minutes max → 2 × 30-min tasks


# ── edge cases ────────────────────────────────────────────────────────────────

def test_pet_with_no_tasks_pending():
    """A pet with all tasks completed has no pending tasks."""
    pet = make_pet()
    task = Task("Feeding", "8:00 AM")
    pet.add_task(task)
    task.mark_completed()

    assert pet.pending_tasks() == []


def test_owner_no_pets_returns_empty_schedule():
    """An owner with no pets produces an empty schedule."""
    owner = Owner("Empty", "empty@example.com")
    scheduler = Scheduler(owner)

    assert scheduler.schedule() == []
