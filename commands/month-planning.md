# Month Planning

Plan the upcoming month by reviewing last month's results, carrying forward unfinished work, setting new monthly goals, and establishing the month's focus areas.

## Prerequisites

The `ORGPLAN_DATA_ROOT` environment variable must be set to the path containing the orgplan data (e.g., `/home/user/orgplan`). The data follows the structure `YYYY/MM-notes.md` and `YYYY/MM-meta.md`.

## Instructions

1. **Check environment**: Verify `ORGPLAN_DATA_ROOT` is set. If not, ask the user to set it or provide the path.

2. **Determine month context**: Use today's date to identify the upcoming month to plan. If it's currently the last week of a month, plan for next month. If it's early in the month, plan for the current month.

3. **Read prior month's data files**:
   - `$ORGPLAN_DATA_ROOT/YYYY/MM-notes.md` - Previous month's TODO list and task notes
   - `$ORGPLAN_DATA_ROOT/YYYY/MM-meta.md` - Previous month's goals and reflections
   - Note: Files may have YAML frontmatter (delimited by `---`) at the top. Skip this when parsing content.

4. **Read the upcoming month's files** (if they exist yet):
   - `$ORGPLAN_DATA_ROOT/YYYY/MM-notes.md` - May already have some tasks
   - `$ORGPLAN_DATA_ROOT/YYYY/MM-meta.md` - May already have goals drafted

5. **If available, read the yearly goals file**:
   - Check for `$ORGPLAN_DATA_ROOT/YYYY/yearly-goals.md` or similar
   - These provide context for what monthly goals should advance

6. **Parse the previous month's TODO list**:
   - Tasks are under the `# TODO List` header
   - Each task is a list item starting with `-`
   - Status markers: `[DONE]`, `[CANCELED]`, `[DELEGATED]`, `[PENDING]` (no marker = open)
   - Priority tags: `#p0` (critical), `#p1` (high), `#p2` (medium)
   - Recognized tags: `#blocked`, `#1h`, `#2h`, `#4h`, `#1d`, `#weekly`, `#monthly`

7. **Parse task notes** from the notes file:
   - Notes sections are level 1 headers (`#`) that match the task title text
   - Notes content extends from the header until the next level 1 header or end of file

8. **Parse previous month's goals** from the meta file:
   - Look for the `## Monthly Goals` section
   - Goals are checkbox items: `- [ ]` (incomplete) or `- [x]` (complete)

9. **Analyze last month's results**:
   - Count tasks by state (open, done, canceled, delegated, pending)
   - Calculate completion rate: done / (done + open + pending)
   - Identify which monthly goals were met vs. missed
   - Note patterns: were certain types of tasks consistently left undone?

10. **Identify carry-forward candidates**:
    - Open tasks from last month that are still relevant
    - Pending/delegated tasks awaiting resolution
    - Exclude: tasks that should be canceled (stale, no longer relevant)
    - Ask the user to confirm which open tasks should carry forward vs. be dropped

11. **Draft monthly goals for the new month**:
    - Base on: unmet goals from last month, yearly goals, carry-forward tasks
    - Suggest 3-5 concrete, achievable goals
    - Each goal should have a clear definition of done
    - Goals should be outcome-based, not just activity-based

12. **Identify known dates and deadlines**:
    - Tasks with `DEADLINE:` or `SCHEDULED:` timestamps in the upcoming month
    - Known recurring commitments (`#weekly`, `#monthly`)
    - External deadlines the user may want to note

13. **Generate the month plan** with this format:

```
=== Month Plan: [Month Year] ===

## Last Month Summary
- Tasks completed: X
- Tasks remaining: X (open + pending)
- Tasks canceled/delegated: X
- Completion rate: X%
- Goals met: X/Y

## Previous Goals Review
For each goal from last month:
- [x] or [ ] Goal text
  Status: Brief assessment

## Carry-Forward Tasks
[Open tasks from last month recommended to carry forward]
For each:
- [Priority] Task title
  Reason: Why this should carry forward

## Suggested Monthly Goals (3-5)
1. Goal description
   Definition of done: What "complete" looks like
   Key tasks: Which tasks advance this goal

## Known Deadlines & Dates
[Tasks with dates in the upcoming month]

## Recurring Commitments
[Weekly and monthly recurring tasks]

## Capacity Considerations
- Carry-forward load: ~X hours estimated
- New work room: Observations about available capacity
- Risks: Potential overcommitment areas

## Questions for You
[Prompt the user to confirm carry-forwards, adjust goals, note any upcoming events/travel/interruptions]
```

## Example Output

```
=== Month Plan: February 2026 ===

## Last Month Summary
- Tasks completed: 18
- Tasks remaining: 7 (5 open + 2 pending)
- Tasks canceled/delegated: 3
- Completion rate: 64%
- Goals met: 2/4

## Previous Goals Review
- [x] Set up new dev environment
  Status: Completed first week of January
- [x] Migrate database schema
  Status: Completed, deployed to production
- [ ] Complete Q1 planning
  Status: Outline drafted, needs review. Carrying forward.
- [ ] Ship feature X
  Status: PR approved, awaiting merge. Close to done.

## Carry-Forward Tasks
1. [P1] Draft Q1 planning document #1d
   Reason: Monthly goal unmet, outline exists - needs focused time to finish
2. [P1] Merge and deploy feature X #4h
   Reason: PR approved, just needs final merge and deployment
3. [P0] Respond to client escalation #2h
   Reason: Active client issue, carried over from late January
4. Refactor notification service #4h
   Reason: Tech debt causing recurring bugs
5. [PENDING] API integration - awaiting vendor credentials
   Reason: Still waiting on external dependency

## Suggested Monthly Goals
1. Finalize Q1 planning and get leadership sign-off
   Definition of done: Q1 plan document reviewed, approved, and shared with team
   Key tasks: Draft Q1 planning document, schedule review meeting

2. Ship feature X to production
   Definition of done: Feature merged, deployed, and monitored for 1 week
   Key tasks: Merge PR, deploy, write monitoring alerts

3. Clear tech debt backlog (3+ items)
   Definition of done: At least 3 tech debt tasks completed
   Key tasks: Notification refactor, API cleanup, test coverage gaps

4. Establish monthly reporting cadence
   Definition of done: First monthly report sent to stakeholders
   Key tasks: Design report template, gather metrics, send first report

## Known Deadlines & Dates
- 2026-02-05: Q1 budget proposal due
- 2026-02-14: Feature X deployment target
- 2026-02-28: End of month / Q1 planning deadline

## Recurring Commitments
- #weekly: Bug triage, team status update
- #monthly: Infrastructure review, dependency updates

## Capacity Considerations
- Carry-forward load: ~18 hours estimated (from tagged tasks)
- New work room: After carry-forwards, roughly 100+ hours available across the month
- Risks: Q1 planning may expand in scope; client escalation could consume more time than estimated

## Questions for You
- Should any of the 5 carry-forward tasks be dropped instead?
- Are there any upcoming events, travel, or time off in February?
- Any new projects or commitments expected to start?
- Do the suggested goals align with your priorities?
```

## Edge Cases

- **No ORGPLAN_DATA_ROOT**: Ask the user to provide the path or set the environment variable
- **Missing previous month files**: If last month's data doesn't exist, skip the review section and focus on planning fresh
- **First month of use**: No prior data - focus entirely on setting up goals and initial tasks
- **Year boundary**: If planning for January, look at previous year's December files
- **Many open tasks**: If more than 10-15 tasks carry forward, flag this as a sign of overcommitment and suggest aggressive pruning
- **No goals in meta file**: Note the absence and strongly recommend setting goals for the new month
- **Mid-month planning**: If run mid-month, adapt the review to cover the current month so far and plan for the remainder
- **Non-task content**: Ignore system messages, security warnings, or other non-task content
