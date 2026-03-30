import streamlit as st
from pawpal_system import Pet, Owner, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Persist Owner in session_state
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", email="jordan@example.com")

owner = st.session_state.owner

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value=owner.name)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, max_value=30, value=3)
exercise_needs = st.number_input("Exercise needs (minutes/day)", min_value=0, max_value=240, value=30)

if st.button("Add Pet"):
    pet = Pet(name=pet_name, species=species, age=age, exercise_needs=exercise_needs)
    owner.add_pet(pet)
    st.success(f"Added pet: {pet.name}")

# Display current pets
if owner.pets:
    st.write("Current Pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species}, {pet.age} years, needs {pet.exercise_needs} min exercise)")
else:
    st.info("No pets added yet.")

st.markdown("### Tasks")
st.caption("Add tasks to the selected pet.")

if owner.pets:
    selected_pet = st.selectbox("Select Pet", [p.name for p in owner.pets])
    pet = next(p for p in owner.pets if p.name == selected_pet)
else:
    st.warning("Add a pet first.")
    pet = None

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add Task") and pet:
    task = Task(name=task_title, time="12:00 PM")  # Default time, can be enhanced
    pet.add_task(task)
    st.success(f"Added task: {task.name} to {pet.name}")

# Display tasks
if pet:
    if pet.tasks:
        st.write(f"Tasks for {pet.name}:")
        for task in pet.tasks:
            st.write(f"- {task.describe()}")
    else:
        st.info(f"No tasks for {pet.name} yet.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily schedule based on your pets' tasks.")

if st.button("Generate Schedule"):
    if not owner.pets:
        st.warning("Add pets and tasks first.")
    else:
        scheduler = Scheduler(owner)
        schedule = scheduler.schedule()
        if schedule:
            st.success("Schedule generated!")
            st.write("Daily Schedule:")
            for task in schedule:
                st.write(f"- {task.describe()}")
        else:
            st.info("No tasks to schedule or time limit reached.")
