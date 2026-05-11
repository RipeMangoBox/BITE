"""MinerU API client for deep table/formula extraction.

MinerU is a DL-driven PDF parser that excels at:
- Table detection + content extraction (HTML/CSV output)
- Formula detection + LaTeX conversion
- Reading-order reconstruction for dual-column PDFs
- Figure/table region bounding boxes

This client wraps the mineru.net cloud API. Free tier: 5000 files / 1000 pages per day.

API endpoints:
- POST /file_parse  — synchronous (legacy, simpler)
- POST /tasks       — asynchronous (submit → poll → retrieve)
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

# MinerU cloud API base URL
DEFAULT_BASE_URL = "https://mineru.net/api/v1"

# Polling config for async /tasks endpoint
POLL_INTERVAL_SEC = 3.0
POLL_TIMEOUT_SEC = 300.0


@dataclass
class MinerUTable:
    """Structured table extracted by MinerU."""
    caption: str = ""
    table_index: int = 0
    page_num: int = 0
    html: str = ""       # Full table as HTML
    csv: str = ""        # Table as CSV (when available)
    confidence: float = 0.0  # Detection confidence


@dataclass
class MinerUFormula:
    """LaTeX formula extracted by MinerU."""
    latex: str = ""
    page_num: int = 0
    location: str = ""  # "inline" or "display"
    confidence: float = 0.0


@dataclass
class MinerUResult:
    """Structured output from MinerU API."""
    success: bool = False
    markdown: str = ""           # Full document as markdown
    tables: list[MinerUTable] = field(default_factory=list)
    formulas: list[MinerUFormula] = field(default_factory=list)
    figures: list[dict] = field(default_factory=list)
    reading_order: list[int] = field(default_factory=list)  # page sequence
    metadata: dict = field(default_factory=dict)
    error: str = ""


class MinerUClient:
    """Async client for MinerU cloud API.

    Usage:
        client = MinerUClient(api_key="...")
        result = await client.parse_pdf("/path/to/paper.pdf")
        for table in result.tables:
            print(table.html)
    """

    def __init__(
        self,
        api_key: str = "",
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 120.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    @property
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    # ── Public API ─────────────────────────────────────────────────

    async def parse_pdf(self, pdf_path: str | Path) -> MinerUResult:
        """Parse a PDF file with MinerU. Returns structured tables, formulas, markdown."""
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            return MinerUResult(success=False, error=f"File not found: {pdf_path}")

        try:
            return await self._parse_sync(pdf_path)
        except httpx.HTTPStatusError as e:
            logger.warning("MinerU HTTP %s: %s", e.response.status_code, e)
            return MinerUResult(success=False, error=f"HTTP {e.response.status_code}")
        except httpx.TimeoutException:
            logger.warning("MinerU timeout for %s", pdf_path.name)
            return MinerUResult(success=False, error="timeout")
        except Exception as e:
            logger.warning("MinerU parse failed for %s: %s", pdf_path.name, e)
            return MinerUResult(success=False, error=str(e)[:200])

    async def _parse_sync(self, pdf_path: Path) -> MinerUResult:
        """Use POST /file_parse (synchronous endpoint)."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            with open(pdf_path, "rb") as f:
                files = {"file": (pdf_path.name, f, "application/pdf")}
                resp = await client.post(
                    f"{self.base_url}/file_parse",
                    headers=self._headers,
                    files=files,
                )
                resp.raise_for_status()

            data = resp.json()
            return self._parse_response(data)

    async def _parse_async(self, pdf_path: Path) -> MinerUResult:
        """Use POST /tasks → GET /tasks/{task_id} polling (async endpoint).

        Better for large PDFs that exceed the sync timeout.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # 1. Submit task
            with open(pdf_path, "rb") as f:
                files = {"file": (pdf_path.name, f, "application/pdf")}
                submit = await client.post(
                    f"{self.base_url}/tasks",
                    headers=self._headers,
                    files=files,
                )
                submit.raise_for_status()

            task = submit.json()
            task_id = task.get("task_id") or task.get("id")
            if not task_id:
                return MinerUResult(success=False, error="No task_id in response")

            # 2. Poll for completion
            elapsed = 0.0
            while elapsed < POLL_TIMEOUT_SEC:
                await asyncio.sleep(POLL_INTERVAL_SEC)
                elapsed += POLL_INTERVAL_SEC

                status_resp = await client.get(
                    f"{self.base_url}/tasks/{task_id}",
                    headers=self._headers,
                )
                status_resp.raise_for_status()
                status = status_resp.json()

                state = status.get("status") or status.get("state", "")
                if state in ("completed", "done", "success"):
                    # 3. Fetch result
                    result_resp = await client.get(
                        f"{self.base_url}/tasks/{task_id}/result",
                        headers=self._headers,
                    )
                    result_resp.raise_for_status()
                    return self._parse_response(result_resp.json())
                elif state in ("failed", "error"):
                    return MinerUResult(
                        success=False,
                        error=status.get("error", "Unknown error"),
                    )

            return MinerUResult(success=False, error="async polling timeout")

    # ── Response parsing ───────────────────────────────────────────

    def _parse_response(self, data: dict) -> MinerUResult:
        """Parse MinerU API response into MinerUResult."""
        result = MinerUResult(success=True)

        # Full markdown
        result.markdown = data.get("markdown") or data.get("content") or ""

        # Tables
        tables_raw = data.get("tables") or data.get("table_list") or []
        for i, t in enumerate(tables_raw):
            result.tables.append(MinerUTable(
                caption=t.get("caption") or t.get("table_caption", ""),
                table_index=t.get("index") or t.get("table_index", i),
                page_num=t.get("page_num") or t.get("page", 0),
                html=t.get("html") or t.get("table_html", ""),
                csv=t.get("csv") or t.get("table_csv", ""),
                confidence=t.get("confidence") or t.get("score", 0.0),
            ))

        # Formulas
        formulas_raw = data.get("formulas") or data.get("formula_list") or []
        for f in formulas_raw:
            result.formulas.append(MinerUFormula(
                latex=f.get("latex") or f.get("formula", ""),
                page_num=f.get("page_num") or f.get("page", 0),
                location=f.get("location") or f.get("type", "display"),
                confidence=f.get("confidence") or f.get("score", 0.0),
            ))

        # Reading order
        result.reading_order = data.get("reading_order") or data.get("page_order") or []

        # Metadata
        result.metadata = data.get("metadata") or data.get("meta") or {}

        return result


# ── Module-level convenience ──────────────────────────────────────

_client: Optional[MinerUClient] = None


def get_mineru_client(api_key: str = "") -> MinerUClient | None:
    """Return a MinerUClient if api_key is configured, else None."""
    global _client
    if _client is not None:
        return _client if _client.api_key else None
    from backend.config import settings  # deferred import to avoid circular

    key = api_key or getattr(settings, "mineru_api_key", "")
    base_url = getattr(settings, "mineru_base_url", "") or DEFAULT_BASE_URL
    if not key:
        return None
    _client = MinerUClient(api_key=key, base_url=base_url)
    return _client
