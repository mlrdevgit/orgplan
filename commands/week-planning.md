# Week Planning

Plan the upcoming week by reviewing open tasks, approaching deadlines, monthly goal alignment, and workload balance. Produces a prioritized weekly plan.

## Prerequisites

The `ORGPLAN_DATA_ROOT` environment variable must be set to the path containing the orgplan data (e.g., `/home/user/orgplan`). The data follows the structure `YYYY/MM-notes.md` and `YYYY/MM-meta.md`.

## Instructions

1. **Check environment**: Verify `ORGPLAN_DATA_ROOT` is set. If not, ask the user to set it or provide the path.

2. **Determine current date context**: Use today's date to find the current year, month, and day of week. Identify the date range for the upcoming week (next Monday through Friday, or next 7 days if run mid-week).

3. **Read the data files** for the current month (and next month if the week spans a month boundary):
   - `$ORGPLAN_DATA_ROOT/YYYY/MM-notes.md` - Contains the TODO list and task notes
   - `$ORGPLAN_DATA_ROOT/YYYY/MM-meta.md` - Contains monthly goals and reflections
   - If the week crosses into the next month, also read next month's files if they exist
   - Note: Files may have YAML frontmatter (delimited by `---`) at the top. Skip this when parsing content.

4. **Parse the TODO list** from the notes file:
   - Tasks are under the `# TODO List` header
   - Each task is a list item starting with `-`
   - Status markers: `[DONE]`, `[CANCELED]`, `[DELEGATED]`, `[PENDING]` (no marker = open)
   - Priority tags: `#p0` (critical), `#p1` (high), `#p2` (medium)
   - Recognized tags: `#blocked`, `#1h`, `#2h`, `#4h`, `#1d`, `#weekly`, `#monthly`
   - Custom tags (like `#hobby`, `#project-name`) may also appear

5. **Parse task notes** from the notes file:
   - After the TODO list, tasks may have detailed notes in their own sections
   - Notes sections are level 1 headers (`#`) that match the task title text
   - Notes content extends from the header until the next level 1 header or end of file

6. **Parse monthly goals** from the meta file:
   - Look for the `## Monthly Goals` section (level 2 header)
   - Goals are checkbox items: `- [ ]` (incomplete) or `- [x]` (complete)

7. **Identify deadline-sensitive tasks**:
   - Tasks with `DEADLINE:` or `SCHEDULED:` timestamps falling within the next 7 days
   - Tasks with `DEADLINE:` timestamps already past (overdue)
   - Sort by urgency (overdue first, then by deadline date)

8. **Estimate workload**:
   - Use time estimate tags (`#1h`, `#2h`, `#4h`, `#1d`) to roughly size tasks
   - Tasks without estimates: treat as unknown (flag for the user)
   - Sum up estimated hours for open, non-blocked tasks
   - A typical work week is ~30-35 hours of focused task work (not 40 - meetings and overhead exist)

9. **Categorize open tasks into weekly buckets**:
   - **Must do**: P0 tasks, tasks with deadlines this week, overdue tasks
   - **Should do**: P1 tasks, tasks aligned with monthly goals, tasks with deadlines next week
   - **Could do**: P2 tasks, untagged tasks, tasks without deadlines
   - **Blocked**: Tasks with `#blocked` tag (note what's needed to unblock)

10. **Check for recurring tasks**:
    - Tasks tagged `#weekly` that are still open
    - Tasks tagged `#monthly` that haven't been addressed yet

11. **Generate the weekly plan** with this format:

```
=== Week Plan: [Start Date] - [End Date] ===

## Monthly Goals Status
[List incomplete goals with brief progress notes]

## This Week's Deadlines
[Tasks with deadlines this week, sorted by date]

## Must Do (P0 / Deadlines / Overdue)
1. [Priority] Task title [estimate if tagged]
   Why: deadline, critical priority, or overdue

## Should Do (P1 / Goal-aligned)
1. [Priority] Task title [estimate if tagged]
   Goal: which monthly goal this advances

## Could Do (if time permits)
1. Task title [estimate if tagged]

## Blocked (needs attention)
- Task title - what's blocking it

## Workload Estimate
- Must do: ~X hours
- Should do: ~X hours
- Total estimated: ~X hours
- Available capacity: ~30-35 hours
- Assessment: [under/balanced/overloaded]

## Recurring Tasks Due
[Weekly and monthly recurring tasks that need attention]

## Suggested Daily Distribution
Brief suggestion of how to spread tasks across the week:
- Monday: [high-priority items, start-of-week tasks]
- Tuesday-Thursday: [deep work blocks, larger tasks]
- Friday: [wrap-up items, weekly recurring tasks, planning]
```

## Example Output

```
=== Week Plan: 3 February - 7 February 2026 ===

## Monthly Goals Status
- [ ] Complete Q1 planning - outline drafted, needs review and finalization
- [ ] Ship feature X - PR approved, pending merge and deployment
- [x] Set up new dev environment - complete

## This Week's Deadlines
- [P0] Submit Q1 budget proposal - DEADLINE: 2026-02-05 (Wednesday)
- [P1] Feature X deployment - SCHEDULED: 2026-02-06 (Thursday)

## Must Do
1. [P0] Submit Q1 budget proposal #4h
   Why: Hard deadline Wednesday, requires finance review
2. [P0] Respond to client escalation #2h
   Why: Carried over from last week, client waiting
3. [P1] Feature X deployment #4h
   Why: Scheduled Thursday, blocks downstream work

## Should Do
1. [P1] Draft Q1 planning document #1d
   Goal: Advances "Complete Q1 planning"
2. [P1] Write integration tests for feature X #4h
   Goal: Part of "Ship feature X" - needed before deployment
3. [P1] Review team's design proposals #2h
   Goal: Supports team velocity

## Could Do
1. #p2 Update API documentation #2h
2. Refactor notification service #4h
3. Research new monitoring tools #2h

## Blocked
- "Deploy to staging" - waiting on infra team (follow up Monday standup)
- "API integration" - waiting on vendor credentials (send reminder Monday)

## Workload Estimate
- Must do: ~10 hours
- Should do: ~14 hours
- Total estimated: ~24 hours (plus unestimated tasks)
- Available capacity: ~30-35 hours
- Assessment: Balanced - room for 1-2 "could do" items or unexpected work

## Recurring Tasks Due
- #weekly Review and triage incoming bug reports
- #weekly Update team status document

## Suggested Daily Distribution
- Monday: Client escalation (fresh start), unblock staging deploy, weekly triage
- Tuesday: Q1 budget proposal (deep work), integration tests
- Wednesday: Q1 budget proposal finalize & submit, design review
- Thursday: Feature X deployment, Q1 planning document
- Friday: Q1 planning continued, weekly status update, plan next week
```

## Edge Cases

- **No ORGPLAN_DATA_ROOT**: Ask the user to provide the path or set the environment variable
- **Missing files**: Work with what's available; note missing files
- **Month boundary**: If the week spans two months, check both months' files. Note that next month's file may not exist yet
- **No open tasks**: Suggest using the week for strategic thinking, goal-setting, or tackling longer-term projects
- **Heavily overloaded**: If estimated hours exceed capacity, explicitly recommend which "should do" items to defer and flag the overload
- **All tasks blocked**: Focus the plan on unblocking actions rather than task execution
- **No time estimates**: Note which tasks lack estimates and suggest the user add them for better planning
- **Weekend/holiday**: If run on a weekend, plan for the following Monday-Friday
- **Non-task content**: Ignore system messages, security warnings, or other non-task content
