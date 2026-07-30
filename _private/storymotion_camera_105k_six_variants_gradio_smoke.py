#!/usr/bin/env python3
"""Browser smoke for the Camera-105K plus Pulp seven-system Gradio tab."""
from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import Page, sync_playwright


URL = os.environ.get("STORYMOTION_GRADIO_URL", "http://127.0.0.1:17865")
TAB = "Camera 105K + Pulp · Seven systems"
SECOND_SAMPLE = "2017_H1TQv3qA7PI_00018_001_a"
SCREENSHOT = Path("/tmp/storymotion_camera_105k_pulp_seven_systems.png")
HEADINGS = (
    "C3-25 · former baseline · 105K · joint-parallel",
    "v9 · Camera 105K · joint-parallel",
    "v11 C0-LAT · co-mainline · Camera 105K · sequential",
    "v11 C0-GEO · co-mainline · Camera 105K · sequential",
    "v11 C1-LAT · Camera 105K · sequential",
    "v11 C1-GEO · Camera 105K · sequential",
    "PulpMotion official · native step 92,950 · joint",
)


def media_sources(page: Page) -> list[str]:
    sources = []
    for video in page.locator("video:visible").all():
        source = video.get_attribute("src")
        assert source, "visible video has no src"
        sources.append(urljoin(page.url, source))
    return sources


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1900, "height": 1300})
    page_errors: list[str] = []
    console_errors: list[str] = []
    failed_requests: list[str] = []
    page.on("pageerror", lambda error: page_errors.append(str(error)))
    page.on(
        "console",
        lambda message: console_errors.append(message.text)
        if message.type == "error"
        else None,
    )
    page.on(
        "requestfailed",
        lambda request: failed_requests.append(f"{request.url}: {request.failure}"),
    )
    page.goto(URL, wait_until="networkidle", timeout=120_000)
    tabs = page.get_by_role("tab").all_inner_texts()
    assert TAB in tabs, tabs
    page.get_by_role("tab", name=TAB, exact=True).click()
    page.locator("video:visible").first.wait_for(timeout=30_000)
    page.wait_for_timeout(1_500)

    for heading in HEADINGS:
        assert page.get_by_role("heading", name=heading, exact=True).is_visible(), heading
    assert page.get_by_text("v11 四臂：", exact=False).is_visible()
    assert page.get_by_text("PulpMotion official：", exact=False).is_visible()
    assert page.get_by_text("sequential Human→Camera", exact=False).is_visible()
    metric_rows = page.locator(".camera-metrics tbody tr")
    metric_row_count = metric_rows.count()
    assert metric_row_count == 14, metric_row_count
    assert page.get_by_text("Camera system metric index", exact=True).is_visible()
    first_sources = media_sources(page)
    assert len(first_sources) == 7, first_sources
    assert len(set(first_sources)) == 7, first_sources
    for source in first_sources:
        response = page.request.get(source)
        assert response.ok, (source, response.status)
        assert "video" in response.headers.get("content-type", ""), response.headers

    sample = page.locator('[role="combobox"]:visible')
    sample.click()
    options = page.get_by_role("option").all_inner_texts()
    assert len(options) == 8, options
    page.get_by_role("option", name=SECOND_SAMPLE, exact=True).click()
    page.wait_for_function(
        "sampleId => document.body.innerText.includes('Fixed-ID #2 · ' + sampleId)",
        arg=SECOND_SAMPLE,
        timeout=15_000,
    )
    second_sources = media_sources(page)
    assert len(second_sources) == 7, second_sources
    assert first_sources != second_sources, (first_sources, second_sources)
    page.wait_for_function(
        """() => [...document.querySelectorAll('video')]
        .filter((video) => video.offsetParent !== null)
        .every((video) => Number.isFinite(video.duration) && video.duration > 0)""",
        timeout=30_000,
    )
    durations = page.locator("video:visible").evaluate_all(
        "videos => videos.map((video) => video.duration)"
    )
    assert max(durations) - min(durations) < 0.05, durations
    widths = page.locator("video:visible").evaluate_all(
        "videos => videos.map((video) => video.getBoundingClientRect().width)"
    )
    assert max(widths) - min(widths) < 2.0, widths

    page.locator("button:visible").filter(has_text="同步播放当前组").click()
    page.wait_for_function(
        """() => [...document.querySelectorAll('video')]
        .filter((video) => video.offsetParent !== null)
        .every((video) => !video.paused && video.currentTime > 0)""",
        timeout=10_000,
    )
    page.screenshot(path=str(SCREENSHOT), full_page=True)
    browser.close()

payload = {
    "url": URL,
    "tab": TAB,
    "tab_count": len(tabs),
    "sample_options": len(options),
    "videos": len(second_sources),
    "metric_rows": metric_row_count,
    "video_durations": durations,
    "video_widths": widths,
    "sample": SECOND_SAMPLE,
    "page_errors": page_errors,
    "console_errors": console_errors,
    "failed_requests": failed_requests,
    "screenshot": str(SCREENSHOT),
}
print(json.dumps(payload, ensure_ascii=False, indent=2))
assert not page_errors, payload
assert not console_errors, payload
unexpected = [failure for failure in failed_requests if "ERR_ABORTED" not in failure]
assert not unexpected, payload
