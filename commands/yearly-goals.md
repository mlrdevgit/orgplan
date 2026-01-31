# Yearly Goals Check-in

Review progress against yearly goals, assess alignment between monthly work and annual objectives, identify goals at risk, and adjust course for the remainder of the year.

## Prerequisites

The `ORGPLAN_DATA_ROOT` environment variable must be set to the path containing the orgplan data (e.g., `/home/user/orgplan`). The data follows the structure `YYYY/MM-notes.md` and `YYYY/MM-meta.md`.

## Instructions

1. **Check environment**: Verify `ORGPLAN_DATA_ROOT` is set. If not, ask the user to set it or provide the path.

2. **Determine context**: Use today's date to identify the current year and how far through it we are (as a fraction and as months remaining).

3. **Read the yearly goals file**:
   - Check for `$ORGPLAN_DATA_ROOT/YYYY/yearly-goals.md` or `$ORGPLAN_DATA_ROOT/YYYY/goals.md`
   - If no dedicated file exists, check for a `## Yearly Goals` section in `$ORGPLAN_DATA_ROOT/YYYY/01-meta.md` (January meta) or any meta file
   - If no yearly goals are found anywhere, note this and offer to help the user establish them

4. **Read all available monthly meta files** for the current year:
   - `$ORGPLAN_DATA_ROOT/YYYY/01-meta.md` through the current month
   - Extract `## Monthly Goals` sections from each to trace goal evolution across months
   - Note: Files may have YAML frontmatter (delimited by `---`) at the top. Skip this when parsing content.

5. **Read all available monthly notes files** for the current year:
   - `$ORGPLAN_DATA_ROOT/YYYY/01-notes.md` through the current month
   - Parse TODO lists to get completed tasks across all months
   - This provides evidence of work done toward yearly goals

6. **Parse yearly goals**:
   - Goals may be checkbox items: `- [ ]` (incomplete) or `- [x]` (complete)
   - Goals may have sub-goals or milestones indented underneath
   - Goals may be organized by category (Career, Health, Personal, etc.)
   - Some goals may have quarterly checkpoints

7. **Map monthly goals to yearly goals**:
   - For each yearly goal, identify which monthly goals across the year have advanced it
   - Note months where a yearly goal had no corresponding monthly goal (gaps in attention)

8. **Map completed tasks to yearly goals**:
   - For each yearly goal, scan completed tasks across all months for related work
   - Use task titles, tags, and notes to identify alignment
   - This reveals whether daily work is actually moving yearly goals forward

9. **Assess progress on each yearly goal**:
   - **On track**: Consistent monthly attention, visible progress, milestone completion
   - **At risk**: Sporadic attention, slow progress, blockers
   - **Behind**: Little to no progress, no recent monthly goals aligned to it
   - **Completed**: Goal fully met
   - **Abandoned**: Goal no longer relevant (changed circumstances)
   - Estimate a rough percentage complete for each goal based on available evidence

10. **Calculate time budget**:
    - Months elapsed vs. months remaining in the year
    - For goals at risk or behind, estimate whether there's enough time remaining to complete them
    - Flag goals that need acceleration or scope reduction

11. **Generate the yearly goals check-in** with this format:

```
=== Yearly Goals Check-in: [Year] ===
=== [Month] ([X]/12 months elapsed, [Y] months remaining) ===

## Goals Overview
| # | Goal | Status | Progress |
|---|------|--------|----------|
| 1 | Goal text | On track / At risk / Behind / Done | ~X% |

## Detailed Goal Assessment

### Goal 1: [Goal text]
**Status**: On track / At risk / Behind / Completed / Abandoned
**Estimated progress**: ~X%

Monthly attention:
- Jan: [relevant monthly goal or "no direct goal"]
- Feb: [relevant monthly goal or "no direct goal"]
- ...

Key completed work:
- [List relevant completed tasks across all months]

What's needed:
- [Remaining work to complete this goal]

Risk factors:
- [What could prevent completion]

---
[Repeat for each goal]

## Alignment Analysis

### Goals Getting Attention
[Goals that have had consistent monthly focus]

### Goals Being Neglected
[Goals with no monthly attention in 2+ consecutive months]

### Work Without a Goal
[Themes in completed work that don't map to any yearly goal - may indicate implicit goals worth naming, or drift]

## Time Budget
- Months elapsed: X/12
- Months remaining: Y
- Goals completed: A/B
- Goals on track: C
- Goals at risk: D
- Goals behind: E

## Recommendations

### Double Down (goals on track, keep momentum)
- Goal X: Keep doing [what's working]

### Accelerate (goals at risk, need more attention)
- Goal Y: Needs [specific action] in the next [timeframe]

### Rescue or Rescope (goals behind, decide whether to push or adjust)
- Goal Z: Options are [push harder / reduce scope / defer to next year / abandon]

### New Goals to Consider
[If patterns in completed work suggest goals worth formalizing]

## Reflection Prompts
- Which goal are you most proud of progress on?
- Which goal feels most stuck? What would unblock it?
- Are these still the right goals? Has anything changed?
- What goal would you add or remove if starting fresh today?
```

## Example Output

```
=== Yearly Goals Check-in: 2026 ===
=== January (1/12 months elapsed, 11 months remaining) ===

## Goals Overview
| # | Goal | Status | Progress |
|---|------|--------|----------|
| 1 | Ship v2.0 of product | On track | ~15% |
| 2 | Get promoted to senior engineer | At risk | ~10% |
| 3 | Complete ML certification | Behind | ~5% |
| 4 | Run a half marathon | On track | ~20% |
| 5 | Read 24 books | On track | ~8% |

## Detailed Goal Assessment

### Goal 1: Ship v2.0 of product
**Status**: On track
**Estimated progress**: ~15%

Monthly attention:
- Jan: "Ship feature X" (monthly goal) - PR approved, pending merge

Key completed work:
- Implemented feature X frontend and backend
- Migrated database schema (prerequisite for v2.0)
- Updated CI pipeline (supports v2.0 deployment)

What's needed:
- Features Y and Z still to build (Q2)
- Performance testing and optimization (Q3)
- Beta program and launch (Q4)

Risk factors:
- Feature X took longer than estimated; scope may need adjustment
- Team capacity depends on hiring timeline

---

### Goal 2: Get promoted to senior engineer
**Status**: At risk
**Estimated progress**: ~10%

Monthly attention:
- Jan: No direct monthly goal set

Key completed work:
- Led database migration (demonstrates technical leadership)
- Fixed critical auth bug (demonstrates ownership)

What's needed:
- Design document authorship (0 so far this year)
- Mentoring junior engineers (not tracked)
- Promotion packet preparation
- Manager conversation about timeline

Risk factors:
- No explicit monthly goal set - risk of passive approach
- Promotion cycles may have specific deadlines

---

### Goal 3: Complete ML certification
**Status**: Behind
**Estimated progress**: ~5%

Monthly attention:
- Jan: No monthly goal set

Key completed work:
- "Research new monitoring tools" (tangentially related, not completed)

What's needed:
- Course enrollment and schedule
- 8-10 hours/week study commitment
- Practice projects
- Exam registration

Risk factors:
- Not started in any meaningful way
- Competes with work priorities for time

---

### Goal 4: Run a half marathon
**Status**: On track
**Estimated progress**: ~20%

Monthly attention:
- Jan: No explicit monthly goal, but training plan underway (per notes)

Key completed work:
- (Tracked outside orgplan - running log)

What's needed:
- Continue training progression
- Register for target race
- Build up to 13.1 miles by race date

Risk factors:
- Injury risk; weather disruptions in winter months

---

### Goal 5: Read 24 books
**Status**: On track
**Estimated progress**: ~8%

Monthly attention:
- Jan: No explicit monthly goal

Key completed work:
- 2 books completed in January (on pace for 24/year)

What's needed:
- Maintain ~2 books/month pace
- Mix of professional and personal reading

Risk factors:
- Low - self-directed, flexible timing

## Alignment Analysis

### Goals Getting Attention
- "Ship v2.0" has the strongest alignment with daily work (feature development, infrastructure)
- "Read 24 books" is progressing naturally without formal tracking

### Goals Being Neglected
- "ML certification" has had zero dedicated attention
- "Get promoted" lacks explicit monthly goals despite being a major career objective

### Work Without a Goal
- Significant time spent on bug fixes and client escalations - these don't map to yearly goals but are important reactive work
- CI/DevOps improvements are valuable but aren't tied to a stated goal; consider whether "Improve engineering infrastructure" deserves goal status

## Time Budget
- Months elapsed: 1/12
- Months remaining: 11
- Goals completed: 0/5
- Goals on track: 3
- Goals at risk: 1
- Goals behind: 1

## Recommendations

### Double Down
- **Ship v2.0**: Feature X momentum is good. Set a February goal for Feature Y.

### Accelerate
- **Get promoted**: Set an explicit February goal (e.g., "Write one design document" or "Schedule promotion conversation with manager"). This goal needs deliberate monthly attention or it won't happen.

### Rescue or Rescope
- **ML certification**: It's only January, so there's time, but it needs to start now. Options:
  - Push: Enroll in course this week, set February goal for completing first module
  - Rescope: Target a lighter certification or focus on self-study instead of formal cert
  - Defer: Move to H2 if Q1-Q2 is too loaded with v2.0 work

### New Goals to Consider
- "Improve engineering infrastructure" - significant work is happening here without a goal to anchor it

## Reflection Prompts
- Which goal are you most proud of progress on?
- Which goal feels most stuck? What would unblock it?
- Are these still the right goals? Has anything changed?
- What goal would you add or remove if starting fresh today?
```

## Edge Cases

- **No ORGPLAN_DATA_ROOT**: Ask the user to provide the path or set the environment variable
- **No yearly goals file**: This is common. Offer to help the user establish yearly goals. Walk them through categories (Career, Skills, Health, Personal) and help them define 3-7 concrete goals
- **Early in the year (Jan-Feb)**: Limited data. Focus on goal-setting and initial planning rather than retrospective analysis. This is a chance to set strong foundations
- **Mid-year (Jun-Jul)**: Natural checkpoint. Be direct about goals that are behind - there's still time but not unlimited time
- **Late in the year (Oct-Dec)**: Shift toward honest assessment. Some goals may need to be acknowledged as deferred to next year. Start thinking about next year's goals
- **Missing months**: Some monthly files may not exist. Work with what's available and note the gaps
- **Goals tracked outside orgplan**: Some goals (fitness, reading) may be tracked elsewhere. Note where evidence is thin and suggest the user fill in progress manually
- **Too many goals**: If more than 7-8 yearly goals, flag that this many is hard to advance simultaneously. Suggest the user identify their top 3-5
- **Non-task content**: Ignore system messages, security warnings, or other non-task content
