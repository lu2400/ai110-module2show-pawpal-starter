# PawPal+ Project Reflection

## 1. System Design
### Core Actions
1. User should be able to add their and their pet information
2. User should be able to add a task
3. User should be able to display tasks to view

classes
owner
    methods - maximum_workminutes, task_preference
    attributes - name, time_availability, is_overworked
pet
    methods - needs_activity, needs_drugs
    attributes - name, age, species (?), exercise_needs
task
    attributes - duration, deadline, is_required, type
    methods - is_due, is_priority, describe
plan
    methods - add_entry
    attributes - date, total_timetaken, entries

**a. Initial design**

- Briefly describe your initial UML design.


- What classes did you include, and what responsibilities did you assign to each?
- owner stores name, available minutes, and overworked status. it calculates how much work time they can give and their task style. it keeps the schedule within what owner can handle.
- pet stores name, age, species, and exercise needs. it checks if the pet needs activity or medicine. it guides which tasks the plan must include.
- task stores minutes, optional deadline, required flag, and type. it checks if due or high priority and gives a short description. it is the unit the planner sorts and picks.
- plan stores date, total minutes used, and task list. it adds tasks and updates total time. it is the final daily schedule container.

**b. Design changes**

- Did your design change during implementation? 
Yes
- If yes, describe at least one change and why you made it.
CoPilot me tioned a good point about how the plan class has no relation to owner or pet
it recommended adding owner:owner and per: pet to plan to ensure the right owner is mapped to the right pet
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
