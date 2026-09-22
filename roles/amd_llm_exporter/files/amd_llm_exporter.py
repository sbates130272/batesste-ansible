#!/usr/bin/env python3
"""Prometheus exporter for AMD LLM API (Anthropic) token usage statistics."""

import logging
import os
import sys
import threading
import time
from datetime import datetime, timedelta, timezone

import requests
from prometheus_client import Counter, Gauge, start_http_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)

ENDPOINT = os.environ.get(
    "AMD_LLM_EXPORTER_ENDPOINT", "https://llm-api.amd.com/api/UsageStats"
)
PORT = int(os.environ.get("AMD_LLM_EXPORTER_PORT", "9876"))
WINDOW_DAYS = int(os.environ.get("AMD_LLM_EXPORTER_WINDOW_DAYS", "30"))
REFRESH_SECONDS = int(os.environ.get("AMD_LLM_EXPORTER_REFRESH_SECONDS", "300"))

# ANTHROPIC_CUSTOM_HEADER holds the full "Header-Name: value" string.
_RAW_HEADER = os.environ.get("ANTHROPIC_CUSTOM_HEADER", "")

# Aggregate gauges
_total_requests = Gauge("amd_llm_total_requests", "Total API requests in window")
_total_tokens = Gauge("amd_llm_total_tokens", "Total tokens in window")
_approx_charge_usd = Gauge(
    "amd_llm_approx_charge_usd", "Approximate charge in USD in window"
)
_window_days = Gauge("amd_llm_window_days", "Reporting window length in days")

# Per-provider/model gauges
_LABELS = ["provider", "model"]
_model_requests = Gauge("amd_llm_model_requests", "Requests per model", _LABELS)
_model_prompt_tokens = Gauge(
    "amd_llm_model_prompt_tokens", "Prompt tokens per model", _LABELS
)
_model_completion_tokens = Gauge(
    "amd_llm_model_completion_tokens", "Completion tokens per model", _LABELS
)
_model_total_tokens = Gauge(
    "amd_llm_model_total_tokens", "Total tokens per model", _LABELS
)
_model_charge_usd = Gauge(
    "amd_llm_model_approx_charge_usd", "Approximate charge in USD per model", _LABELS
)

# Operational metrics
_fetch_errors = Counter(
    "amd_llm_fetch_errors_total", "Cumulative fetch errors since start"
)
_last_fetch_ts = Gauge(
    "amd_llm_last_fetch_timestamp_seconds", "Unix timestamp of last successful fetch"
)


def _parse_auth_header(raw: str) -> dict[str, str]:
    """Split 'Header-Name: value' into a dict suitable for requests."""
    if ":" not in raw:
        log.error(
            "ANTHROPIC_CUSTOM_HEADER must be 'Header-Name: value', got: %r", raw
        )
        sys.exit(1)
    name, _, value = raw.partition(":")
    return {name.strip(): value.strip()}


def _fetch_and_update(auth_headers: dict[str, str]) -> None:
    now = datetime.now(tz=timezone.utc)
    start = (now - timedelta(days=WINDOW_DAYS)).strftime("%Y-%m-%d")
    end = now.strftime("%Y-%m-%d")

    try:
        resp = requests.get(
            ENDPOINT,
            params={"start": start, "end": end},
            headers=auth_headers,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        log.error("Fetch failed: %s", exc)
        _fetch_errors.inc()
        return

    _total_requests.set(data.get("totalRequests", 0))
    _total_tokens.set(data.get("totalTokens", 0))
    _approx_charge_usd.set(data.get("approxChargeInUSD", 0))
    _window_days.set(WINDOW_DAYS)

    for provider, entries in data.get("stats", {}).items():
        for entry in entries:
            model = entry["model"]
            _model_requests.labels(provider, model).set(entry.get("totalRequests", 0))
            _model_prompt_tokens.labels(provider, model).set(
                entry.get("promptTokens", 0)
            )
            _model_completion_tokens.labels(provider, model).set(
                entry.get("completionTokens", 0)
            )
            _model_total_tokens.labels(provider, model).set(
                entry.get("totalTokens", 0)
            )
            _model_charge_usd.labels(provider, model).set(
                entry.get("approxChargeInUSD", 0)
            )

    _last_fetch_ts.set(time.time())
    log.info(
        "Updated: requests=%d tokens=%d charge=$%.2f window=%s..%s",
        data.get("totalRequests", 0),
        data.get("totalTokens", 0),
        data.get("approxChargeInUSD", 0),
        start,
        end,
    )


def _refresh_loop(auth_headers: dict[str, str]) -> None:
    while True:
        _fetch_and_update(auth_headers)
        time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    if not _RAW_HEADER:
        log.error("ANTHROPIC_CUSTOM_HEADER is not set")
        sys.exit(1)

    auth_headers = _parse_auth_header(_RAW_HEADER)

    start_http_server(PORT)
    log.info("Metrics available on :%d/metrics", PORT)

    threading.Thread(target=_refresh_loop, args=(auth_headers,), daemon=True).start()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        log.info("Exiting")
