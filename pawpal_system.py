from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional


@dataclass
class Task:
    name: str
    time: str
    frequency: Optional[str] = None
    completed: bool = False
    description: Optional[str] = None
    due_date: Optional[date] = None

    def __post_init__(self):
        """Set description to name if not provided. Default due_date to today."""
        if self.description is None:
            self.description = self.name
        if self.due_date is None:
            self.due_date = date.today()

    def is_due(self, now: Optional[datetime] = None) -> bool:
        """Check if the task is due based on the scheduled time."""
        if now is None:
            now = datetime.now()
        try:
            target = datetime.strptime(self.time, "%I:%M %p")
            target = target.replace(year=now.year, month=now.month, day=now.day)
            return now >= target
        except ValueError:
            return False

    def is_priority(self) -> bool:
        """Determine if the task is high priority."""
        return self.frequency == "daily" or "med" in (self.description or "").lower()

    def describe(self) -> str:
        """Return a string description of the task."""
        flag = "✅" if self.completed else "⬜"
        freq = f" ({self.frequency})" if self.frequency else ""
        date_str = f" on {self.due_date}" if self.due_date else ""
        return f"{flag} {self.description} at {self.time}{date_str}{freq}"

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    age: int
    exercise_needs: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        self.tasks.append(task)

    def pending_tasks(self) -> List[Task]:
        """Return a list of pending tasks."""
        return [t for t in self.tasks if not t.completed]

    def completed_tasks(self) -> List[Task]:
        """Return a list of completed tasks."""
        return [t for t in self.tasks if t.completed]

    def needs_activity(self) -> bool:
        """Check if the pet needs activity based on tasks."""
        return any(t.description.lower() == "exercise" and not t.completed for t in self.tasks)


class Owner:
    def __init__(self, name: str, email: str, time_availability: int = 240, is_overworked: bool = False):
        self.name = name
        self.email = email
        self.time_availability = time_availability
        self.is_overworked = is_overworked
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def all_tasks(self) -> List[Task]:
        """Return all tasks from all pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def pending_tasks(self) -> List[Task]:
        """Return all pending tasks from all pets."""
        return [t for t in self.all_tasks() if not t.completed]

    def maximum_workminutes(self) -> int:
        """Calculate the maximum work minutes available."""
        if self.is_overworked:
            return int(self.time_availability * 0.5)
        return self.time_availability

    def task_preference(self) -> List[str]:
        """Return the list of task preferences."""
        return ["medication", "feeding", "exercise", "grooming", "play"]

    def filter_tasks(self, completed=None, pet_name=None) -> List[Task]:
        """Filter tasks by completion status and/or pet name.
        
        Args:
            completed: If True, return completed tasks; if False, pending; if None, all.
            pet_name: If provided, filter to tasks for that pet; if None, all pets.
        
        Returns:
            List of filtered tasks.
        """
        tasks = self.all_tasks()
        
        if pet_name is not None:
            tasks = [t for pet in self.pets if pet.name == pet_name for t in pet.tasks]
        
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        
        return tasks


class Scheduler:

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their scheduled time."""
        return sorted(tasks, key=lambda t: t.time)

    def __init__(self, owner: Owner):
        self.owner = owner

    def gather_tasks(self) -> List[Task]:
        """Gather all pending tasks from the owner."""
        return self.owner.pending_tasks()

    def prioritize(self, tasks: List[Task]) -> List[Task]:
        """Prioritize the list of tasks."""
        def sort_key(t: Task):
            pri = 0
            if t.is_priority():
                pri -= 10
            if t.is_due():
                pri -= 5
            return (not t.completed, pri, t.time)

        return sorted(tasks, key=sort_key)

    def schedule(self, max_minutes: Optional[int] = None) -> List[Task]:
        """Generate a schedule of tasks within time limits."""
        max_minutes = max_minutes if max_minutes is not None else self.owner.maximum_workminutes()
        schedule: List[Task] = []
        used = 0

        for task in self.prioritize(self.gather_tasks()):
            estimated = 30
            if used + estimated > max_minutes:
                break
            schedule.append(task)
            used += estimated

        return schedule

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task as completed and auto-schedule the next occurrence for recurring tasks.

        For "daily" tasks, the next due date is always today + 1 day, anchored
        to the current date rather than the original due date so that late
        completions don't cascade into the past.

        For "weekly" tasks, the next due date is the original due date + 7 days,
        preserving the day-of-week cadence.

        The new task is appended to the same pet's task list automatically.

        Args:
            task: The task to mark as completed.

        Returns:
            The newly created next-occurrence Task for recurring tasks,
            or None if the task has no frequency set.
        """
        task.mark_completed()

        if task.frequency not in ("daily", "weekly"):
            return None

        if task.frequency == "daily":
            next_due = date.today() + timedelta(days=1)
        else:
            next_due = task.due_date + timedelta(days=7)

        next_task = Task(
            name=task.name,
            time=task.time,
            frequency=task.frequency,
            description=task.description,
            due_date=next_due,
        )

        for pet in self.owner.pets:
            if task in pet.tasks:
                pet.add_task(next_task)
                break

        return next_task

    def find_conflicts(self, tasks: Optional[List[Task]] = None) -> Dict[str, List[Task]]:
        """Detect scheduling conflicts by finding tasks that share the same time slot.

        Compares tasks across all pets by default, or against a caller-supplied
        list. Uses a single O(n) pass to group tasks by their time string, then
        filters to only the slots where two or more tasks overlap.

        Args:
            tasks: Tasks to check. Defaults to all tasks across all of the
                   owner's pets if not provided.

        Returns:
            A dict mapping each conflicting time string to the list of tasks
            scheduled at that time. Empty dict means no conflicts.
        """
        if tasks is None:
            tasks = self.owner.all_tasks()

        time_groups: Dict[str, List[Task]] = {}
        for task in tasks:
            time_groups.setdefault(task.time, []).append(task)

        return {time: group for time, group in time_groups.items() if len(group) > 1}
