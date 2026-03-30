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
it recommended adding owner:owner and pet: pet to plan to ensure the right owner is mapped to the right pet
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
it assigns 30 minutes to every task regardless.

- Why is that tradeoff reasonable for this scenario?
i was trying to prioritise the owner's time.
assuming some tasks will take longer than others, schedule tries to avoid giving the owner too many tasks.
Better for the owner to have some free time than none at all before needing to do something important.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
i mostly used a combination of Copilot and Claude. I used Copilot for planning, it was just a bit more helpful than Claude. I used Claude for debugging and brainstorming primarily. 

- What kinds of prompts or questions were most helpful?
The tools were extremely helpful when I already had a plan before prompting. Generating ideas with AI from scratch never really works out quite well. Hvaing something to base off of helps with ensuring you're generating what you want and now what the AI tool wants.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When I used inline chats to start off main.py, it kept suggesting functions that were not in my pawpal_system.py file even though it was referenced. It just kept messing it up.

- How did you evaluate or verify what the AI suggested?
It was easy to evaluate/verufy because the .py file simply wouldn't run until i fixed the issues.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I mainly tested sorting, behaviour, conflicts, and scheduling.
I tried to ensure tasks were sortedby time, recurring tasks, flagged double scheduling, priority tasks were done first and ownder isnt overworked.

- Why were these tests important?
this was to ensure the scheduler would actually give good suggestions and the owner could adequately use the app everyday.

**b. Confidence**

- How confident are you that your scheduler works correctly?
4 out of 5. all 21 tests pass. the one gap is sort_by_time uses string comparison so "9:00 AM" sorts after "10:00 AM". there is a test that documents the bug but it is not fixed yet.

- What edge cases would you test next if you had more time?
what happens when complete_task is called on a task that belongs to no pet. and whether the conflict warning in the UI actually blocks a bad schedule from being used.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
the conflict detection. running find_conflicts in two places, right after adding a task and again when generating the schedule, made the UI more useful without a lot of extra code.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
i would add a duration field to Task. it was in the original UML but did not make it into the final code. without it the scheduler assumes every task takes 30 minutes which is not realistic.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
- having a design before prompting makes a big difference. when i came to the AI with a clear structure it gave useful output. when i started from nothing it generated things that did not match the rest of the project. the AI works better as a collaborator on your plan than as the person making the plan.
