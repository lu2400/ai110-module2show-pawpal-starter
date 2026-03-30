from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional


@dataclass
class Task:
    duration: int  # in minutes
    deadline: Optional[datetime] = None
    is_required: bool = False
    task_type: str = ""

    def is_due(self) -> bool:
        pass

    def is_priority(self) -> bool:
        pass

    def describe(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    age: int
    species: str
    exercise_needs: int  # in minutes per day

    def needs_activity(self) -> bool:
        pass

    def needs_drugs(self) -> bool:
        pass


class Owner:
    def __init__(self, name: str, time_availability: int, is_overworked: bool = False):
        self.name = name
        self.time_availability = time_availability  # in minutes per day
        self.is_overworked = is_overworked

    def maximum_workminutes(self) -> int:
        pass

    def task_preference(self) -> str:
        pass


class Plan:
    def __init__(self, plan_date: date):
        self.date = plan_date
        self.total_timetaken = 0  # in minutes
        self.entries: List[Task] = []

    def add_entry(self, task: Task) -> None:
        pass