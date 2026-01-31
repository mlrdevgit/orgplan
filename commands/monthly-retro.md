# Monthly Retro

Conduct a structured retrospective on the past month: analyze what was accomplished, what fell through, identify patterns in productivity, and extract actionable insights for improvement.

## Prerequisites

The `ORGPLAN_DATA_ROOT` environment variable must be set to the path containing the orgplan data (e.g., `/home/user/orgplan`). The data follows the structure `YYYY/MM-notes.md` and `YYYY/MM-meta.md`.

## Instructions

1. **Check environment**: Verify `ORGPLAN_DATA_ROOT` is set. If not, ask the user to set it or provide the path.

2. **Determine retro scope**: Use today's date to identify which month to retrospect. If it's the first week of a month, retro the previous month. Otherwise, retro the current month so far.

3. **Read the data files** for the month under review:
   - `$ORGPLAN_DATA_ROOT/YYYY/MM-notes.md` - Contains the TODO list and task notes
   - `$ORGPLAN_DATA_ROOT/YYYY/MM-meta.md` - Contains monthly goals and reflections
   - Note: Files may have YAML frontmatter (delimited by `---`) at the top. Skip this when parsing content.

4. **Optionally read the previous month** for comparison:
   - `$ORGPLAN_DATA_ROOT/YYYY/(MM-1)-notes.md` - For trend comparison
   - This helps identify whether metrics improved or declined

5. **Parse the TODO list** from the notes file:
   - Tasks are under the `# TODO List` header
   - Each task is a list item starting with `-`
   - Status markers: `[DONE]`, `[CANCELED]`, `[DELEGATED]`, `[PENDING]` (no marker = open)
   - Priority tags: `#p0` (critical), `#p1` (high), `#p2` (medium)
   - Recognized tags: `#blocked`, `#1h`, `#2h`, `#4h`, `#1d`, `#weekly`, `#monthly`
   - Custom tags (like `#hobby`, `#project-name`) may also appear

6. **Parse task notes** from the notes file:
   - Notes sections are level 1 headers (`#`) that match the task title text
   - Notes content extends from the header until the next level 1 header or end of file

7. **Parse monthly goals** from the meta file:
   - Look for the `## Monthly Goals` section
   - Goals are checkbox items: `- [ ]` (incomplete) or `- [x]` (complete)

8. **Compute metrics**:
   - **Total tasks**: Count all tasks in the TODO list
   - **By state**: done, open, canceled, delegated, pending
   - **Completion rate**: done / (done + open + pending) as percentage
   - **Cancellation rate**: canceled / total as percentage
   - **By priority**: breakdown of P0/P1/P2/untagged tasks and their completion rates
   - **Estimated vs. actual**: if tasks have time estimate tags, sum estimated hours for done tasks
   - **Goal completion**: goals met / total goals

9. **Identify patterns**:
   - **What types of tasks got done?** Look at tags and priorities of completed tasks
   - **What types stalled?** Look at tags and priorities of tasks still open
   - **Blocked tasks**: How many are blocked? Are they the same ones from last month?
   - **Priority discipline**: Were P0 tasks actually completed first, or did lower-priority work creep in?
   - **Scope creep**: Estimate how many tasks were likely added mid-month (tasks without time estimates, tasks near the bottom of the list)
   - **Delegation effectiveness**: Were delegated tasks resolved or still pending?

10. **Analyze goal outcomes**:
    - For each monthly goal, determine: met, partially met, or not addressed
    - Identify why goals were missed (overcommitment, scope change, blocked, deprioritized)
    - Note which completed tasks contributed to goals vs. were unrelated to any goal

11. **Generate the monthly retro** with this format:

```
=== Monthly Retrospective: [Month Year] ===

## Metrics Dashboard
| Metric | Value |
|--------|-------|
| Total tasks | X |
| Completed | X (Y%) |
| Open (remaining) | X |
| Canceled | X |
| Delegated | X |
| Pending | X |
| Goals met | X/Y |

## Goal Outcomes
For each goal:
- [x] or [ ] or [~] Goal text
  Outcome: What happened. Met / Partially met / Not addressed
  Reason: Brief explanation

## Accomplishments
[List all completed tasks, grouped by theme or priority]

### Highlights
[2-3 most impactful completions with brief context on why they matter]

## What Remained Open
[Open tasks with analysis]
- [Priority] Task title [estimate]
  Why open: Brief explanation (blocked, deprioritized, underestimated, added late)

## Patterns Observed

### What Went Well
[2-3 patterns that supported productivity]
- Example: "P0 tasks were consistently completed within the first week"

### What Didn't Go Well
[2-3 patterns that hindered productivity]
- Example: "Tasks without time estimates tended to stall"

### Priority Discipline
[Were high-priority tasks actually prioritized?]
- P0 completion rate: X%
- P1 completion rate: X%
- P2 completion rate: X%

## Blocked Items Analysis
[Persistent blockers and their duration]
- Task title - blocker description
  Duration: How long it's been blocked
  Impact: What's affected by this blocker

## Actionable Takeaways
[3-5 specific, actionable changes for next month]
1. Takeaway (e.g., "Add time estimates to all new tasks to improve planning accuracy")
2. Takeaway (e.g., "Limit carry-forward tasks to 5 to avoid backlog accumulation")

## Reflection Prompts
- What was your biggest win this month?
- What was your biggest frustration?
- If you could change one thing about how you worked this month, what would it be?
- Rate your month 1-10 and briefly explain why.
```

## Example Output

```
=== Monthly Retrospective: January 2026 ===

## Metrics Dashboard
| Metric | Value |
|--------|-------|
| Total tasks | 28 |
| Completed | 18 (64%) |
| Open (remaining) | 5 |
| Canceled | 3 |
| Delegated | 1 |
| Pending | 1 |
| Goals met | 2/4 |

## Goal Outcomes
- [x] Set up new dev environment
  Outcome: Met. Completed first week of January.
- [x] Migrate database schema
  Outcome: Met. Deployed to production successfully.
- [~] Complete Q1 planning
  Outcome: Partially met. Outline drafted but not reviewed or finalized.
  Reason: Competing P0 priorities pushed this back repeatedly.
- [ ] Ship feature X
  Outcome: Not complete, but close. PR approved, awaiting merge.
  Reason: Code review took longer than expected; merge deferred to February.

## Accomplishments

### Infrastructure & DevOps
- [DONE] Set up new dev environment
- [DONE] Migrate database schema
- [DONE] Update CI pipeline configuration
- [DONE] Configure monitoring alerts

### Feature Work
- [DONE] Implement feature X frontend
- [DONE] Write feature X backend API
- [DONE] Feature X code review (submitted)

### Bug Fixes
- [DONE] Fix production auth bug
- [DONE] Fix notification race condition
- [DONE] Patch API rate limiting issue

### Highlights
1. **Database migration** - Zero-downtime migration of 2M+ records, no incidents
2. **Auth bug fix** - Resolved critical production issue affecting 15% of users
3. **CI pipeline improvement** - 40% faster builds, saving ~2 hours/week across team

## What Remained Open
- [P1] Draft Q1 planning document #1d
  Why open: Deprioritized multiple times for urgent work; needs dedicated focus block
- [P0] Respond to client escalation #2h
  Why open: Arrived late on Jan 31, carrying to February
- Refactor notification service #4h
  Why open: Nice-to-have tech debt, consistently below the cut line
- [P2] Update API documentation #2h
  Why open: Low priority, no deadline pressure
- Research new monitoring tools #2h
  Why open: Added late in the month, exploratory

## Patterns Observed

### What Went Well
- Infrastructure tasks were completed efficiently and early in the month
- Bug fixes were handled promptly, especially P0 items
- Feature X progressed steadily despite scope being larger than initially estimated

### What Didn't Go Well
- Q1 planning was repeatedly deferred - "important but not urgent" trap
- 3 tasks were canceled (scope changed), suggesting planning wasn't stable
- Tech debt tasks were consistently deprioritized

### Priority Discipline
- P0 completion rate: 83% (5/6)
- P1 completion rate: 67% (8/12)
- P2 completion rate: 50% (3/6)
- Untagged completion rate: 50% (2/4)

## Blocked Items Analysis
- "Deploy to staging" - waiting on infra team provisioning
  Duration: 2+ weeks
  Impact: Blocking feature X staging validation
- "API integration" - waiting on vendor credentials
  Duration: 3+ weeks
  Impact: Blocking partner integration milestone

## Actionable Takeaways
1. **Schedule "important not urgent" work explicitly** - Block calendar time for Q1 planning-type tasks so they don't get perpetually deferred
2. **Escalate blockers after 1 week** - Two items have been blocked 2-3 weeks; set a hard escalation rule
3. **Limit mid-month task additions** - Several tasks added late in the month diluted focus
4. **Add time estimates to all tasks** - 10 tasks had no estimates, making workload planning harder
5. **Dedicate one day/month to tech debt** - Prevents tech debt from accumulating indefinitely

## Reflection Prompts
- What was your biggest win this month?
- What was your biggest frustration?
- If you could change one thing about how you worked this month, what would it be?
- Rate your month 1-10 and briefly explain why.
```

## Edge Cases

- **No ORGPLAN_DATA_ROOT**: Ask the user to provide the path or set the environment variable
- **Missing files**: If notes or meta file doesn't exist, mention this and work with what's available
- **No completed tasks**: Focus the retro on understanding why (overcommitment? wrong tasks? external blockers?) rather than presenting empty metrics
- **All tasks completed**: Highlight the achievement, then examine whether goals were set ambitiously enough
- **No goals set**: Note the absence and recommend setting goals as a key takeaway
- **Mid-month retro**: If run mid-month, present it as a "mid-month check-in" with partial data and a forward-looking tone
- **Very few tasks**: If fewer than 5 total tasks, the month may have been tracked elsewhere or tasks are too coarse-grained. Note this.
- **Previous month comparison**: If previous month's data exists, include trend arrows (up/down) for key metrics
- **Non-task content**: Ignore system messages, security warnings, or other non-task content
