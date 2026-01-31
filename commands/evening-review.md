# Evening Review

Reflect on the day's progress, capture what was accomplished, identify carry-over tasks, and set up tomorrow for a productive start.

## Prerequisites

The `ORGPLAN_DATA_ROOT` environment variable must be set to the path containing the orgplan data (e.g., `/home/user/orgplan`). The data follows the structure `YYYY/MM-notes.md` and `YYYY/MM-meta.md`.

## Instructions

1. **Check environment**: Verify `ORGPLAN_DATA_ROOT` is set. If not, ask the user to set it or provide the path.

2. **Determine current month**: Use today's date to find the current year and month.

3. **Read the data files** for the current month:
   - `$ORGPLAN_DATA_ROOT/YYYY/MM-notes.md` - Contains the TODO list and task notes
   - `$ORGPLAN_DATA_ROOT/YYYY/MM-meta.md` - Contains monthly goals and reflections
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
   - Notes sections are level 1 headers (`#`) that match the task title text (without status markers or priority tags)
   - Notes content extends from the header until the next level 1 header or end of file

6. **Parse monthly goals** from the meta file:
   - Look for the `## Monthly Goals` section (level 2 header)
   - Goals are checkbox items: `- [ ]` (incomplete) or `- [x]` (complete)

7. **Identify today's completed work**:
   - Look for tasks marked `[DONE]` that appear relevant to today (recently completed)
   - Since the file doesn't track completion dates, use context clues: tasks near the top of the done list, tasks the user mentioned working on, or tasks with today's date in notes
   - Ask the user to confirm what they completed today if it's ambiguous

8. **Identify carry-over tasks**:
   - Open tasks that are high priority (`#p0`, `#p1`) but remain unfinished
   - Tasks with deadlines approaching in the next 1-3 days
   - Tasks that were likely planned for today (from morning review or user context) but not completed

9. **Check for newly blocked tasks**:
   - Open tasks with `#blocked` tag
   - Note any tasks that might have become blocked during the day

10. **Assess goal progress**:
    - For each incomplete monthly goal, note whether today's completed work moved it forward
    - Identify goals that haven't had progress recently

11. **Generate the evening review** with this format:

```
=== Evening Review for [Day Month Year] ===

## Today's Accomplishments
[List tasks completed today with brief context on impact]

## Carry-Over to Tomorrow
For each task:
1. [Priority] Task title
   Context: Why it didn't get done / what's needed to complete it

## Blocked Items
[Tasks with #blocked tag or newly identified blockers]
Action needed: What would unblock each item

## Goal Progress
[For each monthly goal, brief status update based on today's work]

## Tomorrow's Setup
[2-3 suggested focus tasks for tomorrow morning, based on priorities and carry-over]

## Quick Reflection
[Prompt the user: "What went well today? Anything you'd do differently?"]
```

## Example Output

```
=== Evening Review for Friday 31 January 2026 ===

## Today's Accomplishments
- [DONE] Fix production bug in auth service - Critical fix deployed, unblocked 3 downstream tasks
- [DONE] Review PR for feature X - Approved with minor comments, moves "Ship feature X" goal forward
- [DONE] Update CI pipeline configuration - Now runs 40% faster

## Carry-Over to Tomorrow
1. [P1] Draft Q1 planning document
   Context: Started outline but ran out of time; needs 2-3 more hours of focused work
2. [P0] Respond to client escalation
   Context: Arrived late in the day; needs fresh attention tomorrow morning

## Blocked Items
- "Deploy to staging" - waiting on infra team to provision new environment
  Action needed: Follow up with infra lead in Monday standup
- "API integration" - waiting on vendor API credentials
  Action needed: Send reminder email to vendor contact

## Goal Progress
- [ ] Complete Q1 planning - IN PROGRESS: outline started today, needs completion
- [ ] Ship feature X - ADVANCING: PR reviewed, merge expected Monday
- [x] Set up new dev environment - Already complete

## Tomorrow's Setup
1. [P0] Respond to client escalation (first thing - fresh eyes)
2. [P1] Draft Q1 planning document (deep work block - 2-3 hours)
3. [P1] Merge feature X PR after addressing review comments

## Quick Reflection
What went well today? Anything you'd do differently?
(Take a moment to note your thoughts - this helps improve future planning)
```

## Edge Cases

- **No ORGPLAN_DATA_ROOT**: Ask the user to provide the path or set the environment variable
- **Missing files**: If notes or meta file doesn't exist for current month, mention this and work with what's available
- **No completed tasks today**: That's okay - note it neutrally and focus on what progress was made (research, unblocking, planning). Avoid judgment
- **Everything completed**: Celebrate the productive day and suggest using tomorrow for strategic/longer-term work
- **End of month**: If tomorrow is a new month, note that tasks will need to be carried forward to the new month's file
- **Friday evening**: Mention that carry-over items will wait until Monday; suggest noting any context that might be forgotten over the weekend
- **Non-task content**: Ignore system messages, security warnings, or other non-task content
