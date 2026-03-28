"""HTTP client for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

import httpx


class ObservabilityClient:
    """Async client for VictoriaLogs and VictoriaTraces HTTP APIs."""

    def __init__(
        self,
        victorialogs_url: str,
        victoriatraces_url: str,
        timeout: float = 30.0,
    ) -> None:
        self.victorialogs_url = victorialogs_url.rstrip("/")
        self.victoriatraces_url = victoriatraces_url.rstrip("/")
        self.timeout = timeout
        self._http_client: httpx.AsyncClient | None = None

    @property
    def http_client(self) -> httpx.AsyncClient:
        """Lazy HTTP client."""
        if self._http_client is None:
            raise RuntimeError("Client not initialized. Use async context manager.")
        return self._http_client

    async def __aenter__(self) -> ObservabilityClient:
        self._http_client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._http_client:
            await self._http_client.aclose()
        self._http_client = None

    async def logs_query(self, query: str, limit: int = 100) -> list[dict]:
        """Query VictoriaLogs using LogsQL.
        
        API: POST /select/logsql/query
        """
        url = f"{self.victorialogs_url}/select/logsql/query"
        response = await self.http_client.post(
            url,
            params={"limit": limit},
            data=query.encode("utf-8"),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        return response.json()

    async def logs_error_count(
        self, service: str | None = None, minutes: int = 60
    ) -> dict:
        """Count errors in VictoriaLogs over a time window.
        
        Uses VictoriaLogs stats endpoint.
        """
        time_filter = f"_time:{minutes}m"
        severity_filter = "severity:ERROR"
        if service:
            query = f'{time_filter} {severity_filter} service.name:"{service}"'
        else:
            query = f"{time_filter} {severity_filter}"
        
        url = f"{self.victorialogs_url}/select/logsql/stats_query"
        response = await self.http_client.get(
            url,
            params={"query": query},
        )
        response.raise_for_status()
        return response.json()

    async def traces_list(self, service: str | None = None, limit: int = 20) -> list[dict]:
        """List recent traces from VictoriaTraces.
        
        API: GET /select/jaeger/api/traces
        """
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces"
        params = {"limit": limit}
        if service:
            params["service"] = service
        
        response = await self.http_client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    async def traces_get(self, trace_id: str) -> dict | None:
        """Get a specific trace by ID.
        
        API: GET /select/jaeger/api/traces/<traceID>
        """
        url = f"{self.victoriatraces_url}/select/jaeger/api/traces/{trace_id}"
        response = await self.http_client.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [None])[0] if data.get("data") else None
