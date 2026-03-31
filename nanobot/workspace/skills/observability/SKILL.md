# Observability Skills — How to Use Logs and Traces Tools

You have access to VictoriaLogs and VictoriaTraces through MCP tools. This skill guide teaches you how to use them effectively for debugging and system health monitoring.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `logs_search` | Search logs in VictoriaLogs using LogsQL queries | `query` (optional, default "*"): LogsQL query string<br>`limit` (optional, default 20): Max entries to return<br>`time_range` (optional, default "1h"): Time range like "1h", "6h", "24h" |
| `logs_error_count` | Count errors per service over a time window | `time_range` (optional, default "1h"): Time window to count errors |
| `traces_list` | List recent traces, optionally filtered by service | `service` (optional): Filter by service name<br>`limit` (optional, default 10): Max traces to return<br>`time_range` (optional, default "1h"): Time range |
| `traces_get` | Fetch a specific trace by ID | `trace_id` (required): The trace ID to fetch |

## Strategy

### When the user asks about errors or system health

1. **Start with error count**: Call `logs_error_count` with an appropriate time range to get a quick overview
2. **If errors found**: Call `logs_search` with `query="level:error"` or `query="severity:ERROR"` to see the actual error messages
3. **Look for trace IDs**: Error logs often contain `trace_id` fields — extract these for deeper investigation
4. **Fetch the trace**: If you found a relevant trace ID, call `traces_get` to see the full request flow and where it failed

### When the user asks about a specific request or operation

1. **Search logs for context**: Call `logs_search` with a query matching the operation, e.g., `event:request_started` or a specific path
2. **Extract trace ID**: From the log results, find the `trace_id` field
3. **Get the full trace**: Call `traces_get` with that trace ID to see the complete span hierarchy

### When the user asks "what's happening in the system"

1. **List recent traces**: Call `traces_list` to see what operations have been running
2. **Check for errors**: Call `logs_error_count` to see if any services are reporting errors
3. **Summarize findings**: Report on system activity and any issues found

## LogsQL Query Tips

VictoriaLogs uses LogsQL for querying. Common patterns:

- `*` — All logs
- `level:error` — Logs with level field equal to "error"
- `severity:ERROR` — Logs with severity field equal to "ERROR"
- `service.name:"backend"` — Logs from a specific service
- `event:db_query` — Logs with a specific event type
- `path:/items/` — Logs containing a specific path
- `_stream:{service.name="backend"}` — Filter by stream labels
- Combine with AND: `service.name:"backend" AND level:error`
- Combine with OR: `level:error OR severity:ERROR`

## Formatting responses

- **Be concise**: Lead with the answer, then offer optional details
- **Summarize, don't dump**: Don't output raw JSON — summarize findings in natural language
- **Include timestamps**: When reporting errors, mention when they occurred
- **Highlight trace IDs**: If a trace ID is relevant, include it so the user can investigate further
- **Use tables**: For multiple errors or traces, use markdown tables

## Example Interactions

### "Any errors in the last hour?"

1. Call `logs_error_count` with `time_range="1h"`
2. If errors found, call `logs_search` with `query="level:error"` to get details
3. Summarize: "Found X errors in the last hour from service Y. The most recent error was..."

### "What went wrong with the last request?"

1. Call `logs_search` with `query="event:request_completed" AND status:500"` to find failed requests
2. Extract the `trace_id` from the most recent failure
3. Call `traces_get` with that trace ID
4. Analyze the trace: "The request failed during the db_query span. The error was..."

### "Show me recent activity"

1. Call `traces_list` with `limit=5` to see recent traces
2. Summarize: "Recent activity includes: [list operations with their durations]"

### "Debug the /items/ endpoint"

1. Call `logs_search` with `query="path:/items/"` and `time_range="1h"`
2. Look for patterns: slow requests, errors, or unusual behavior
3. If you find a problematic trace ID, fetch it with `traces_get`
4. Report: "The /items/ endpoint is working normally" or "Found issues: ..."

## Important Notes

- **Time ranges**: Use appropriate time ranges — "1h" for recent issues, "24h" or "7d" for historical analysis
- **Error correlation**: Logs and traces are correlated via `trace_id` — use this to jump from logs to traces
- **Service names**: The backend service is named "Learning Management Service" in telemetry
- **Graceful degradation**: If VictoriaLogs or VictoriaTraces is unreachable, report the error clearly and suggest checking the observability stack
- **Don't hallucinate**: If no errors are found, say so — don't invent problems

## Troubleshooting

### No logs found

- Check the time range — try expanding it (e.g., "24h" instead of "1h")
- Verify the query syntax — LogsQL is case-sensitive for field values
- The service might not be emitting logs — check if the backend is running

### Trace not found

- The trace might be outside the retention period (default 7 days)
- The trace ID might be malformed — trace IDs are 32-character hex strings
- VictoriaTraces might be unreachable — report this to the user

### Too many results

- Narrow the time range
- Add more specific filters to the query (e.g., `service.name:"backend"`)
- Reduce the limit parameter
