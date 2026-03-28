---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

You have access to LMS MCP tools that query the live Learning Management System. Here's how to use them effectively:

## Available Tools

- `lms_health` - Check if LMS backend is healthy, returns item count
- `lms_labs` - List all available labs (returns lab IDs like "lab-01", "lab-02")
- `lms_learners` - List all registered learners
- `lms_pass_rates` - Get pass rates for a specific lab (requires lab parameter)
- `lms_timeline` - Get submission timeline for a lab (requires lab parameter)
- `lms_groups` - Get group performance for a lab (requires lab parameter)
- `lms_top_learners` - Get top learners by score for a lab (requires lab parameter, optional limit)
- `lms_completion_rate` - Get completion rate (passed/total) for a lab (requires lab parameter)
- `lms_sync_pipeline` - Trigger the LMS sync pipeline

## Strategy Rules

1. If the user asks for scores, pass rates, completion, groups, timeline, or top learners WITHOUT naming a specific lab, you MUST call `lms_labs` first to get the list of available labs.

2. When multiple labs are available, ask the user which lab they want to know about. Do not guess - let them choose.

3. Use each lab's title as the user-facing label when presenting options, unless the tool output gives a better identifier.

4. Format numeric results nicely:
   - Percentages should show one decimal place (e.g., "89.1%")
   - Large numbers can use commas (e.g., "1,234")

5. Keep responses concise. Don't overload with unnecessary details.

6. When the user asks "what can you do?", explain your current tools and limits clearly:
   - You can query real LMS data (labs, learners, pass rates, completion rates, groups, timelines, top learners)
   - You need a lab name for most queries
   - You can check backend health
   - You can trigger sync pipeline

7. If the backend returns no data for a lab (0 total), mention that the lab has no submissions yet and it's not a meaningful comparison.
