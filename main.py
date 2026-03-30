from pawpal_system import *
owner = Owner("Dali", "dalihf@mmail.com")

pet1 = Pet("Bad", "Bunny", 5, 30)
pet2 = Pet("Doja", "Cat", 3, 20)

owner.add_pet(pet1)
owner.add_pet(pet2)

pet1.add_task(Task("Feeding", "8:00 AM"))
pet1.add_task(Task("Playing", "3:00 PM"))
pet2.add_task(Task("Grooming", "10:00 AM"))

print("Today's Schedule:")
for pet in owner.pets:
    print(f"\n{pet.name} ({pet.species}):")
    for task in pet.tasks:
        print(f"  - {task.name} at {task.time}")