import warnings
from pawpal_system import *

owner = Owner("Dali", "dalihf@mmail.com")

pet1 = Pet("Bad", "Bunny", 5, 30)
pet2 = Pet("Doja", "Cat", 3, 20)

owner.add_pet(pet1)
owner.add_pet(pet2)

# Add tasks — two intentionally overlap at 8:00 AM to trigger conflict detection
pet1.add_task(Task("Playing", "3:00 PM"))
pet1.add_task(Task("Feeding", "8:00 AM"))
pet2.add_task(Task("Grooming", "10:00 AM"))
pet2.add_task(Task("Medication", "8:00 AM"))  # conflicts with pet1's Feeding

# Mark one task as completed
pet1.tasks[0].mark_completed()

scheduler = Scheduler(owner)

print("All tasks (unsorted):")
for task in owner.all_tasks():
    print(f"  - {task.describe()}")

print("\nTasks sorted by time:")
sorted_tasks = scheduler.sort_by_time(owner.all_tasks())
for task in sorted_tasks:
    print(f"  - {task.describe()}")

print("\nPending tasks for Bad:")
filtered_tasks = owner.filter_tasks(completed=False, pet_name="Bad")
for task in filtered_tasks:
    print(f"  - {task.describe()}")

print("\nCompleted tasks:")
completed_tasks = owner.filter_tasks(completed=True)
for task in completed_tasks:
    print(f"  - {task.describe()}")

print("\nChecking for schedule conflicts...")
conflicts = scheduler.find_conflicts()
if conflicts:
    for time, tasks in conflicts.items():
        warnings.warn(f"Schedule conflict at {time}: {[t.name for t in tasks]}")
else:
    print("  No conflicts found.")