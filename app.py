import streamlit as st
from pawpal_system import Pet, Owner, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ── constants ─────────────────────────────────────────────────────────────────

PRIORITY_ICON = {"high": "🔴", "medium": "🟡", "low": "🟢"}
SPECIES_ICON  = {"dog": "🐶", "cat": "🐱", "other": "🐾"}

TASK_ICON = {
    "walk":       "🦮",
    "exercise":   "🏃",
    "feed":       "🍖",
    "feeding":    "🍖",
    "medication": "💊",
    "meds":       "💊",
    "groom":      "✂️",
    "grooming":   "✂️",
    "play":       "🎾",
    "vet":        "🏥",
    "bath":       "🛁",
}

def task_emoji(name: str) -> str:
    lower = name.lower()
    for keyword, icon in TASK_ICON.items():
        if keyword in lower:
            return icon
    return "📋"

# ── session state ─────────────────────────────────────────────────────────────

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", email="jordan@example.com")

owner = st.session_state.owner

# ── header ────────────────────────────────────────────────────────────────────

st.title("🐾 PawPal+")
st.caption("Plan your pet's day — sorted by priority, checked for conflicts.")
st.divider()

# ── owner + pet setup ─────────────────────────────────────────────────────────

st.subheader("Your Pets")

with st.form("add_pet_form"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pet_name = st.text_input("Name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with col3:
        age = st.number_input("Age", min_value=0, max_value=30, value=3)
    with col4:
        exercise_needs = st.number_input("Exercise (min/day)", min_value=0, max_value=240, value=30)
    submitted = st.form_submit_button("Add Pet")
    if submitted:
        owner.add_pet(Pet(name=pet_name, species=species, age=age, exercise_needs=exercise_needs))
        st.success(f"Added {SPECIES_ICON.get(species, '🐾')} {pet_name}!")

if owner.pets:
    cols = st.columns(len(owner.pets))
    for col, pet in zip(cols, owner.pets):
        icon = SPECIES_ICON.get(pet.species, "🐾")
        pending = len(pet.pending_tasks())
        done    = len(pet.completed_tasks())
        with col:
            st.metric(label=f"{icon} {pet.name}", value=f"{pending} pending", delta=f"{done} done")
            st.caption(f"{pet.species.title()} · age {pet.age} · {pet.exercise_needs} min/day")
else:
    st.info("No pets added yet.")

st.divider()

# ── task input ────────────────────────────────────────────────────────────────

st.subheader("Add a Task")

if not owner.pets:
    st.warning("Add a pet first.")
    selected_pet = None
else:
    selected_pet_name = st.selectbox("For which pet?", [p.name for p in owner.pets])
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    with st.form("add_task_form"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            task_title = st.text_input("Task", value="Morning walk")
        with col2:
            task_time = st.text_input("Time (e.g. 8:00 AM)", value="8:00 AM")
        with col3:
            frequency = st.selectbox("Frequency", ["none", "daily", "weekly"])
        with col4:
            priority = st.selectbox("Priority", ["high", "medium", "low"], index=1)
        add_task = st.form_submit_button("Add Task")

    if add_task:
        freq = None if frequency == "none" else frequency
        task = Task(name=task_title, time=task_time, frequency=freq, priority=priority)
        selected_pet.add_task(task)
        icon = task_emoji(task_title)
        st.success(f"{icon} **{task.name}** added for {selected_pet.name} — {PRIORITY_ICON[task.priority]} {task.priority.title()} priority at {task.time}.")

# ── task display ──────────────────────────────────────────────────────────────

if selected_pet and selected_pet.tasks:
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(selected_pet.tasks)

    st.markdown(f"#### {SPECIES_ICON.get(selected_pet.species, '🐾')} {selected_pet.name}'s tasks")
    st.caption("Sorted by time · 🔴 High  🟡 Medium  🟢 Low")

    st.table([
        {
            "":          "✅" if t.completed else "⏳",
            "Task":      f"{task_emoji(t.name)} {t.name}",
            "Time":      t.time,
            "Priority":  f"{PRIORITY_ICON.get(t.priority, '🟡')} {t.priority.title()}",
            "Frequency": t.frequency.title() if t.frequency else "—",
            "Due":       str(t.due_date),
        }
        for t in sorted_tasks
    ])

    conflicts = scheduler.find_conflicts()
    if conflicts:
        for time_slot, clashing_tasks in conflicts.items():
            names = " and ".join(
                f"**{t.name}** ({next((p.name for p in owner.pets if t in p.tasks), '?')})"
                for t in clashing_tasks
            )
            st.warning(f"⚠️ **Conflict at {time_slot}:** {names} overlap. Edit one task's time to fix this.")
    else:
        st.success("✅ No scheduling conflicts.")

elif selected_pet:
    st.info(f"No tasks for {selected_pet.name} yet. Add one above.")

st.divider()

# ── schedule generation ───────────────────────────────────────────────────────

st.subheader("📅 Today's Schedule")
st.caption("Tasks are ordered by priority first, then time. Completed tasks are excluded.")

if st.button("Generate Schedule", type="primary"):
    if not owner.pets or not owner.all_tasks():
        st.warning("Add pets and tasks first.")
    else:
        scheduler = Scheduler(owner)

        conflicts = scheduler.find_conflicts()
        if conflicts:
            st.warning("⚠️ **Your schedule has conflicts — fix these for a reliable plan:**")
            for time_slot, clashing_tasks in conflicts.items():
                details = ", ".join(
                    f"{task_emoji(t.name)} {t.name} ({next((p.name for p in owner.pets if t in p.tasks), '?')})"
                    for t in clashing_tasks
                )
                st.markdown(f"- **{time_slot}:** {details}")

        schedule = scheduler.schedule()
        if schedule:
            st.success(f"✅ {len(schedule)} task(s) scheduled within your available time.")

            for i, t in enumerate(schedule, start=1):
                icon = task_emoji(t.name)
                p_icon = PRIORITY_ICON.get(t.priority, "🟡")
                freq_label = f" · 🔁 {t.frequency.title()}" if t.frequency else ""
                with st.container(border=True):
                    col_num, col_info, col_badge = st.columns([0.5, 5, 1.5])
                    with col_num:
                        st.markdown(f"### {i}")
                    with col_info:
                        st.markdown(f"**{icon} {t.name}**")
                        st.caption(f"🕐 {t.time}{freq_label} · 📅 Due {t.due_date}")
                    with col_badge:
                        st.markdown(f"{p_icon} **{t.priority.title()}**")
        else:
            st.info("No tasks fit within the available time.")
