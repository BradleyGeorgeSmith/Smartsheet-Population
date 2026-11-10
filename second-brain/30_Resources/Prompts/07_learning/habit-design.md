# Habit Design (Atomic Habits applied)

**Purpose**: turn a vague intention ("journal every day", "leg press three
times a day", "stop biting nails", "clear emails every day") into a designed
habit with cue, routine, reward, and a tracking line for HabitNow or ClickUp.
**When**: when adding any habit, and at the monthly review for stuck habits.
**Inputs**: `{{intention}}`, `{{current_routine}}`, `{{obstacles}}`.

```text
I want to build this habit: {{intention}}
My current daily routine, roughly: {{current_routine}}
What has stopped me before: {{obstacles}}

Design it using James Clear's four laws (make it obvious, attractive, easy,
satisfying) and habit stacking. Output Markdown:

## Habit statement
"After I [existing habit], I will [new habit, two-minute version] at [place]."
## Make it obvious
Cue, environment change, visual trigger (one line each).
## Make it attractive
Pair it with something I like; who I could do it with.
## Make it easy
The two-minute starter version; friction to remove; what to prepare the
night before.
## Make it satisfying
Immediate reward; how I track it (HabitNow line, ClickUp recurring task,
tick on the whiteboard); the streak rule ("never miss twice").
## Obstacle plan
For each obstacle I listed: an if-then response.
## Review date
When to check whether it stuck, and what "stuck" means in numbers.
## Tracker line
One line formatted for HabitNow: name | frequency | time | reminder text.

Keep medical items as "follow the plan my doctor gave me"; do not add
dosing advice.
```

**Output**: `20_Areas/Habits/<habit>.md` plus the tracker line.
**Source**: James Clear, *Atomic Habits* (four laws, paraphrased); prompt
original.
