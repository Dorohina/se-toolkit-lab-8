"""Async HTTP client, models, and formatters for the LMS backend API."""

import httpx
import json
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class HealthResult(BaseModel):
    status: str
    item_count: int | str = "unknown"
    error: str = ""


class Item(BaseModel):
    id: int | None = None
    type: str = "step"
    parent_id: int | None = None
    title: str = ""
    description: str = ""


class Learner(BaseModel):
    id: int | None = None
    external_id: str = ""
    student_group: str = ""


class PassRate(BaseModel):
    task: str
    avg_score: float
    attempts: int


class TimelineEntry(BaseModel):
    date: str
    submissions: int


class GroupPerformance(BaseModel):
    group: str
    avg_score: float
    students: int


class TopLearner(BaseModel):
    learner_id: int
    avg_score: float
    attempts: int


class CompletionRate(BaseModel):
    lab: str
    completion_rate: float
    passed: int
    total: int


class SyncResult(BaseModel):
    new_records: int
    total_records: int


# ---------------------------------------------------------------------------
# Observability models (VictoriaLogs)
# ---------------------------------------------------------------------------


class LogEntry(BaseModel):
    """A single log entry from VictoriaLogs."""

    timestamp: str = ""
    message: str = ""
    level: str = ""
    service: str = ""
    event: str = ""
    trace_id: str = ""
    span_id: str = ""
    raw: dict = {}


class LogSearchResult(BaseModel):
    """Result of a log search query."""

    entries: list[LogEntry]
    total: int
    query: str


class ErrorCount(BaseModel):
    """Error count for a service."""

    service: str
    count: int
    level: str = "error"


class ErrorCountResult(BaseModel):
    """Result of error count query."""

    errors: list[ErrorCount]
    time_range: str


# ---------------------------------------------------------------------------
# Observability models (VictoriaTraces)
# ---------------------------------------------------------------------------


class TraceSpan(BaseModel):
    """A single span within a trace."""

    trace_id: str = ""
    span_id: str = ""
    parent_span_id: str | None = None
    operation_name: str = ""
    service_name: str = ""
    start_time: int = 0
    duration: int = 0
    tags: list[dict] = []
    logs: list[dict] = []


class Trace(BaseModel):
    """A complete trace with all its spans."""

    trace_id: str
    spans: list[TraceSpan]
    start_time: int = 0
    end_time: int = 0
    duration: int = 0


class TraceSummary(BaseModel):
    """Summary of a trace for listing."""

    trace_id: str
    service_name: str
    operation_name: str
    start_time: int
    duration: int
    span_count: int


class TracesListResult(BaseModel):
    """Result of listing traces."""

    traces: list[TraceSummary]
    total: int


# ---------------------------------------------------------------------------
# HTTP client
# ---------------------------------------------------------------------------


class LMSClient:
    """Client for the LMS backend API."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {api_key}"}

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(headers=self._headers, timeout=10.0)

    async def health_check(self) -> HealthResult:
        async with self._client() as c:
            try:
                r = await c.get(f"{self.base_url}/items/")
                r.raise_for_status()
                items = [Item.model_validate(i) for i in r.json()]
                return HealthResult(status="healthy", item_count=len(items))
            except httpx.ConnectError:
                return HealthResult(
                    status="unhealthy", error=f"connection refused ({self.base_url})"
                )
            except httpx.HTTPStatusError as e:
                return HealthResult(
                    status="unhealthy", error=f"HTTP {e.response.status_code}"
                )
            except Exception as e:
                return HealthResult(status="unhealthy", error=str(e))

    async def get_items(self) -> list[Item]:
        async with self._client() as c:
            r = await c.get(f"{self.base_url}/items/")
            r.raise_for_status()
            return [Item.model_validate(i) for i in r.json()]

    async def get_learners(self) -> list[Learner]:
        async with self._client() as c:
            r = await c.get(f"{self.base_url}/learners/")
            r.raise_for_status()
            return [Learner.model_validate(i) for i in r.json()]

    async def get_pass_rates(self, lab: str) -> list[PassRate]:
        async with self._client() as c:
            r = await c.get(
                f"{self.base_url}/analytics/pass-rates", params={"lab": lab}
            )
            r.raise_for_status()
            return [PassRate.model_validate(i) for i in r.json()]

    async def get_timeline(self, lab: str) -> list[TimelineEntry]:
        async with self._client() as c:
            r = await c.get(f"{self.base_url}/analytics/timeline", params={"lab": lab})
            r.raise_for_status()
            return [TimelineEntry.model_validate(i) for i in r.json()]

    async def get_groups(self, lab: str) -> list[GroupPerformance]:
        async with self._client() as c:
            r = await c.get(f"{self.base_url}/analytics/groups", params={"lab": lab})
            r.raise_for_status()
            return [GroupPerformance.model_validate(i) for i in r.json()]

    async def get_top_learners(self, lab: str, limit: int = 5) -> list[TopLearner]:
        async with self._client() as c:
            r = await c.get(
                f"{self.base_url}/analytics/top-learners",
                params={"lab": lab, "limit": limit},
            )
            r.raise_for_status()
            return [TopLearner.model_validate(i) for i in r.json()]

    async def get_completion_rate(self, lab: str) -> CompletionRate:
        async with self._client() as c:
            r = await c.get(
                f"{self.base_url}/analytics/completion-rate", params={"lab": lab}
            )
            r.raise_for_status()
            return CompletionRate.model_validate(r.json())

    async def sync_pipeline(self) -> SyncResult:
        async with self._client() as c:
            r = await c.post(f"{self.base_url}/pipeline/sync")
            r.raise_for_status()
            return SyncResult.model_validate(r.json())


# ---------------------------------------------------------------------------
# Observability client (VictoriaLogs + VictoriaTraces)
# ---------------------------------------------------------------------------


class ObservabilityClient:
    """Client for VictoriaLogs and VictoriaTraces APIs."""

    def __init__(
        self,
        victorialogs_url: str = "http://victorialogs:9428",
        victoriatraces_url: str = "http://victoriatraces:10428",
    ):
        self.victorialogs_url = victorialogs_url.rstrip("/")
        self.victoriatraces_url = victoriatraces_url.rstrip("/")

    def _logs_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=30.0)

    def _traces_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=30.0)

    def _parse_time_range(self, time_range: str) -> tuple[str, str]:
        """Parse a time range string like '1h' into start/end ISO timestamps."""
        from datetime import datetime, timedelta, timezone

        now = datetime.now(timezone.utc)
        
        # Parse duration
        if time_range.endswith("h"):
            hours = int(time_range[:-1])
            delta = timedelta(hours=hours)
        elif time_range.endswith("d"):
            days = int(time_range[:-1])
            delta = timedelta(days=days)
        elif time_range.endswith("m"):
            minutes = int(time_range[:-1])
            delta = timedelta(minutes=minutes)
        else:
            # Default to 1 hour
            delta = timedelta(hours=1)
        
        start = now - delta
        return start.strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ")

    async def logs_search(
        self, query: str = "*", limit: int = 20, time_range: str = "1h"
    ) -> LogSearchResult:
        """Search logs using LogsQL query."""
        async with self._logs_client() as c:
            try:
                # VictoriaLogs LogsQL query endpoint
                url = f"{self.victorialogs_url}/select/logsql/query"
                start, end = self._parse_time_range(time_range)
                params = {"query": query, "limit": limit, "start": start, "end": end}

                r = await c.get(url, params=params)
                r.raise_for_status()

                # VictoriaLogs returns newline-delimited JSON
                entries = []
                for line in r.text.strip().split("\n"):
                    if line.strip():
                        try:
                            data = json.loads(line)
                            entry = LogEntry(
                                timestamp=data.get("_time", ""),
                                message=data.get("_msg", ""),
                                level=data.get("severity", data.get("level", "")),
                                service=data.get("service.name", data.get("service", "")),
                                event=data.get("event", ""),
                                trace_id=data.get("trace_id", data.get("otelTraceID", "")),
                                span_id=data.get("span_id", data.get("otelSpanID", "")),
                                raw=data,
                            )
                            entries.append(entry)
                        except json.JSONDecodeError:
                            continue

                return LogSearchResult(entries=entries, total=len(entries), query=query)
            except httpx.ConnectError:
                return LogSearchResult(entries=[], total=0, query=query)
            except httpx.HTTPStatusError:
                return LogSearchResult(entries=[], total=0, query=query)
            except Exception:
                return LogSearchResult(entries=[], total=0, query=query)

    async def logs_error_count(
        self, time_range: str = "1h"
    ) -> ErrorCountResult:
        """Count errors per service over a time window."""
        async with self._logs_client() as c:
            try:
                # Query for error-level logs
                query = 'severity:ERROR OR level:error OR level:ERROR'
                url = f"{self.victorialogs_url}/select/logsql/query"
                start, end = self._parse_time_range(time_range)
                params = {"query": query, "limit": 1000, "start": start, "end": end}

                r = await c.get(url, params=params)
                r.raise_for_status()

                # Count errors by service
                error_counts: dict[str, int] = {}
                for line in r.text.strip().split("\n"):
                    if line.strip():
                        try:
                            data = json.loads(line)
                            service = data.get("service.name", data.get("service", "unknown"))
                            error_counts[service] = error_counts.get(service, 0) + 1
                        except json.JSONDecodeError:
                            continue

                errors = [
                    ErrorCount(service=svc, count=count)
                    for svc, count in sorted(error_counts.items(), key=lambda x: -x[1])
                ]
                return ErrorCountResult(errors=errors, time_range=time_range)
            except Exception:
                return ErrorCountResult(errors=[], time_range=time_range)

    async def traces_list(
        self, service: str = "", limit: int = 10, time_range: str = "1h"
    ) -> TracesListResult:
        """List recent traces, optionally filtered by service."""
        async with self._traces_client() as c:
            try:
                # VictoriaTraces native API for trace search
                url = f"{self.victoriatraces_url}/api/v1/traces"
                params = {"limit": limit}

                r = await c.get(url, params=params)
                r.raise_for_status()

                data = r.json()
                traces = []
                for trace_data in data.get("data", []):
                    trace = TraceSummary(
                        trace_id=trace_data.get("traceID", ""),
                        service_name=trace_data.get("serviceName", ""),
                        operation_name=trace_data.get("operationName", ""),
                        start_time=trace_data.get("startTime", 0),
                        duration=trace_data.get("duration", 0),
                        span_count=len(trace_data.get("spans", [])),
                    )
                    traces.append(trace)

                return TracesListResult(traces=traces, total=len(traces))
            except Exception:
                return TracesListResult(traces=[], total=0)

    async def traces_get(self, trace_id: str) -> Trace | None:
        """Fetch a specific trace by ID."""
        async with self._traces_client() as c:
            try:
                url = f"{self.victoriatraces_url}/api/v1/traces/{trace_id}"
                r = await c.get(url)
                r.raise_for_status()

                data = r.json()
                trace_data = data.get("data", {})

                spans = []
                for span_data in trace_data.get("spans", []):
                    span = TraceSpan(
                        trace_id=span_data.get("traceID", ""),
                        span_id=span_data.get("spanID", ""),
                        parent_span_id=span_data.get("parentSpanID"),
                        operation_name=span_data.get("operationName", ""),
                        service_name=span_data.get("serviceName", ""),
                        start_time=span_data.get("startTime", 0),
                        duration=span_data.get("duration", 0),
                        tags=span_data.get("tags", []),
                        logs=span_data.get("logs", []),
                    )
                    spans.append(span)

                # Calculate trace duration
                start_time = min((s.start_time for s in spans), default=0)
                end_time = max((s.start_time + s.duration for s in spans), default=0)

                return Trace(
                    trace_id=trace_id,
                    spans=spans,
                    start_time=start_time,
                    end_time=end_time,
                    duration=end_time - start_time,
                )
            except Exception:
                return None


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------


def format_health(result: HealthResult) -> str:
    if result.status == "healthy":
        return f"\u2705 Backend is healthy. {result.item_count} items available."
    return f"\u274c Backend error: {result.error or 'Unknown'}"


def format_labs(items: list[Item]) -> str:
    labs = sorted(
        [i for i in items if i.type == "lab"],
        key=lambda x: str(x.id),
    )
    if not labs:
        return "\U0001f4ed No labs available."
    text = "\U0001f4da Available labs:\n\n"
    text += "\n".join(f"\u2022 {lab.title}" for lab in labs)
    return text


def format_scores(lab: str, rates: list[PassRate]) -> str:
    if not rates:
        return f"\U0001f4ed No scores found for {lab}."
    text = f"\U0001f4ca Pass rates for {lab}:\n\n"
    text += "\n".join(
        f"\u2022 {r.task}: {r.avg_score:.1f}% ({r.attempts} attempts)" for r in rates
    )
    return text
