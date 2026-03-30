import sys
sys.path.append('..')
import pytest
from pawpal_system import *

def test_task_completion():
    """Verify that mark_completed() changes the task's completed status."""
    task = Task(name="Feed dog", time="8:00 AM")
    assert task.completed == False
    task.mark_completed()
    assert task.completed == True


def test_task_addition_increases_count():
    """Verify that adding a task to a Pet increases the pet's task count."""
    pet = Pet(name="Buddy", species="Dog", age=3, exercise_needs=30)
    initial_count = len(pet.tasks)
    task = Task(name="Walk in park", time="3:00 PM")
    pet.add_task(task)
    assert len(pet.tasks) == initial_count + 1
