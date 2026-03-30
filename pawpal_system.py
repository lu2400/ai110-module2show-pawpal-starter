from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    name: str
    time: str
    frequency: Optional[str] = None
    completed: bool = False
    description: Optional[str] = None

    def __post_init__(self):
        """Set description to name if not provided."""
        if self.description is None:
            self.description = self.name

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
        return f"{flag} {self.description} at {self.time}{freq}"

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


class Scheduler:
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

    def complete_task(self, task: Task) -> None:
        """Mark a task as completed."""
        task.mark_completed()
