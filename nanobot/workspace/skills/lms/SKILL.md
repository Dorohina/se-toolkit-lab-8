# LMS Skills — How to Use LMS Tools

You have access to the LMS (Learning Management System) backend through MCP tools. This skill guide teaches you how to use them effectively.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `lms_health` | Check if the LMS backend is healthy and report the item count | None |
| `lms_labs` | List all labs available in the LMS | None |
| `lms_learners` | List all learners registered in the LMS | None |
| `lms_pass_rates` | Get pass rates (avg score and attempt count per task) for a lab | `lab` (required): Lab identifier |
| `lms_timeline` | Get submission timeline (date + submission count) for a lab | `lab` (required): Lab identifier |
| `lms_groups` | Get group performance (avg score + student count per group) for a lab | `lab` (required): Lab identifier |
| `lms_top_learners` | Get top learners by average score for a lab | `lab` (required), `limit` (optional, default 5) |
| `lms_completion_rate` | Get completion rate (passed / total) for a lab | `lab` (required): Lab identifier |
| `lms_sync_pipeline` | Trigger the LMS sync pipeline. May take a moment | None |

## Strategy

### When the user asks about labs in general

1. **List available labs**: Call `lms_labs` to get the list of all labs
2. **Provide overview**: Summarize what labs exist
3. **Offer to dive deeper**: Ask if they want details about a specific lab

### When the user asks about a specific lab

1. **Check if lab is specified**: If the user doesn't specify which lab, ask them to clarify or list available labs using `lms_labs`
2. **Get completion rate**: Call `lms_completion_rate` with the lab ID
3. **Get pass rates**: Call `lms_pass_rates` for detailed task-level stats
4. **Optional deep dive**: Depending on the question, also call:
   - `lms_groups` for group performance
   - `lms_top_learners` for top students
   - `lms_timeline` for submission patterns

### When the user asks about system health

1. Call `lms_health` to check backend status
2. Report the health status and item count

### When the user asks about learners

1. Call `lms_learners` to get the list of all learners
2. For top performers in a specific lab, use `lms_top_learners`

### Formatting responses

- **Percentages**: Format as `XX.X%` (e.g., `89.1%`)
- **Counts**: Use plain numbers (e.g., `258 students`)
- **Tables**: Use markdown tables for comparative data
- **Be concise**: Lead with the answer, then offer optional details

## Example Interactions

### "What labs are available?"
→ Call `lms_labs`, list them, offer to show details

### "Show me the scores"
→ Ask: "Which lab would you like to see scores for? Here are the available labs: [list from lms_labs]"

### "Which lab has the lowest pass rate?"
→ Call `lms_labs` to get all lab IDs, then call `lms_completion_rate` for each, compare and report

### "How is Lab 02 doing?"
→ Call `lms_completion_rate` for lab-02, then `lms_pass_rates` for details

## Important Notes

- Always validate that a lab exists before querying lab-specific tools
- When a required parameter (like `lab`) is missing from the user's query, ask for clarification
- Lab IDs in the system may be formatted differently (e.g., "Lab 01" vs "lab-01") — use the exact ID from `lms_labs`
- If the LMS backend is unreachable, report the error clearly and suggest checking the backend status
