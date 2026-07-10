"""Download OSS objects referenced by the remote ResearchFlow database.

This mirrors object keys into ``researchflow-backend/storage/`` so a local
``OBJECT_STORAGE_PROVIDER=local`` setup can resolve the same paths.

The default path is efficient for large syncs:
1. Run a downloader inside the remote API container, using the OSS internal
   endpoint and writing into the server's bind-mounted ``./storage``.
2. Rsync that storage tree back to local ``researchflow-backend/storage``.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path
from pathlib import PurePosixPath


REMOTE = "root@47.101.167.55"
REMOTE_DIR = "/opt/researchflow/researchflow-backend"
KEY_PATH = Path(__file__).resolve().parents[2] / "_private" / "aliyun_key" / "autoresearch1.pem"
ROOT = Path(__file__).resolve().parents[1]
STORAGE_DIR = ROOT / "storage"


REMOTE_LIST_SCRIPT = r"""
import asyncio
import json
import os
import oss2
from sqlalchemy import text
from backend.database import async_session

OBJECT_KEY_SQL = '''
WITH object_refs(key) AS (
  SELECT pdf_object_key AS key FROM papers
  WHERE pdf_object_key IS NOT NULL AND pdf_object_key <> ''
  UNION
  SELECT object_key AS key FROM paper_figures
  WHERE object_key IS NOT NULL AND object_key <> ''
  UNION
  SELECT object_key AS key FROM paper_assets
  WHERE object_key IS NOT NULL AND object_key <> ''
  UNION
  SELECT pdf_object_key AS key FROM venue_papers
  WHERE pdf_object_key IS NOT NULL AND pdf_object_key <> ''
)
SELECT DISTINCT key FROM object_refs ORDER BY key
'''

async def main():
    region = os.environ["OBJECT_STORAGE_REGION"]
    bucket = oss2.Bucket(
        oss2.Auth(os.environ["OBJECT_STORAGE_SECRET_ID"], os.environ["OBJECT_STORAGE_SECRET_KEY"]),
        f"https://{region}-internal.aliyuncs.com",
        os.environ["OBJECT_STORAGE_BUCKET"],
    )
    async with async_session() as session:
        rows = (await session.execute(text(OBJECT_KEY_SQL))).fetchall()
    sem = asyncio.Semaphore(int(os.environ.get("RF_OSS_HEAD_WORKERS", "32")))

    async def one(key):
        async with sem:
            head = await asyncio.to_thread(bucket.head_object, key)
            size = int(head.headers.get("Content-Length") or getattr(head, "content_length", 0) or 0)
            return {"key": key, "size": size}

    items = await asyncio.gather(*(one(key) for (key,) in rows))
    for item in sorted(items, key=lambda value: value["key"]):
        print(json.dumps(item, ensure_ascii=False), flush=True)

asyncio.run(main())
"""


REMOTE_MIRROR_SCRIPT = r"""
import asyncio
import os
from pathlib import Path

import oss2
from sqlalchemy import text

from backend.database import async_session

OBJECT_KEY_SQL = '''
WITH object_refs(key) AS (
  SELECT pdf_object_key AS key FROM papers
  WHERE pdf_object_key IS NOT NULL AND pdf_object_key <> ''
  UNION
  SELECT object_key AS key FROM paper_figures
  WHERE object_key IS NOT NULL AND object_key <> ''
  UNION
  SELECT object_key AS key FROM paper_assets
  WHERE object_key IS NOT NULL AND object_key <> ''
  UNION
  SELECT pdf_object_key AS key FROM venue_papers
  WHERE pdf_object_key IS NOT NULL AND pdf_object_key <> ''
)
SELECT DISTINCT key FROM object_refs ORDER BY key
'''

WORKERS = int(os.environ.get("RF_OSS_DOWNLOAD_WORKERS", "8"))

async def main():
    region = os.environ["OBJECT_STORAGE_REGION"]
    bucket = oss2.Bucket(
        oss2.Auth(os.environ["OBJECT_STORAGE_SECRET_ID"], os.environ["OBJECT_STORAGE_SECRET_KEY"]),
        f"https://{region}-internal.aliyuncs.com",
        os.environ["OBJECT_STORAGE_BUCKET"],
    )
    async with async_session() as session:
        rows = (await session.execute(text(OBJECT_KEY_SQL))).fetchall()

    keys = [row[0] for row in rows]
    storage = Path("/app/storage")
    sem = asyncio.Semaphore(WORKERS)
    stats = {"downloaded": 0, "skipped": 0, "errors": 0}

    async def one(idx, key):
        async with sem:
            target = storage / key
            try:
                head = await asyncio.to_thread(bucket.head_object, key)
                size = int(head.headers.get("Content-Length") or getattr(head, "content_length", 0) or 0)
                if target.exists() and target.stat().st_size == size:
                    stats["skipped"] += 1
                    if idx % 100 == 0:
                        print(f"[{idx}/{len(keys)}] skip {key}", flush=True)
                    return
                target.parent.mkdir(parents=True, exist_ok=True)
                tmp = target.with_suffix(target.suffix + ".part")
                await asyncio.to_thread(bucket.get_object_to_file, key, str(tmp))
                actual = tmp.stat().st_size
                if actual != size:
                    tmp.unlink(missing_ok=True)
                    raise RuntimeError(f"expected {size} bytes, got {actual}")
                tmp.replace(target)
                stats["downloaded"] += 1
                print(f"[{idx}/{len(keys)}] download {size} {key}", flush=True)
            except Exception as exc:
                stats["errors"] += 1
                print(f"[{idx}/{len(keys)}] ERROR {key}: {exc}", flush=True)

    await asyncio.gather(*(one(i + 1, key) for i, key in enumerate(keys)))
    print(f"downloaded={stats['downloaded']} skipped={stats['skipped']} errors={stats['errors']}", flush=True)
    if stats["errors"]:
        raise SystemExit(1)

asyncio.run(main())
"""


REMOTE_TAR_STREAM_TEMPLATE = r"""
import json
import os
import sys
import tarfile
import time
from pathlib import PurePosixPath

import oss2

KEYS = __KEYS_JSON__
WORKER = "__WORKER_LABEL__"
PROGRESS_EVERY = int(os.environ.get("RF_OSS_STREAM_PROGRESS_EVERY", "100"))


def validate_key(key):
    path = PurePosixPath(key)
    if key.startswith("/") or ".." in path.parts:
        raise ValueError(f"unsafe object key: {key}")


region = os.environ["OBJECT_STORAGE_REGION"]
bucket = oss2.Bucket(
    oss2.Auth(os.environ["OBJECT_STORAGE_SECRET_ID"], os.environ["OBJECT_STORAGE_SECRET_KEY"]),
    f"https://{region}-internal.aliyuncs.com",
    os.environ["OBJECT_STORAGE_BUCKET"],
)

with tarfile.open(fileobj=sys.stdout.buffer, mode="w|") as tar:
    for idx, key in enumerate(KEYS, 1):
        validate_key(key)
        head = bucket.head_object(key)
        size = int(head.headers.get("Content-Length") or getattr(head, "content_length", 0) or 0)
        obj = bucket.get_object(key)
        info = tarfile.TarInfo(key)
        info.size = size
        info.mtime = int(time.time())
        info.mode = 0o644
        tar.addfile(info, obj)
        if idx == 1 or idx % PROGRESS_EVERY == 0 or idx == len(KEYS):
            print(f"[{WORKER} {idx}/{len(KEYS)}] stream {size} {key}", file=sys.stderr, flush=True)
"""


REMOTE_SIGN_URLS_TEMPLATE = r"""
import json
import os
import sys
from pathlib import PurePosixPath

import oss2

ITEMS = __ITEMS_JSON__
EXPIRES = int(os.environ.get("RF_OSS_SIGN_EXPIRES", "3600"))


def validate_key(key):
    path = PurePosixPath(key)
    if key.startswith("/") or ".." in path.parts:
        raise ValueError(f"unsafe object key: {key}")


region = os.environ["OBJECT_STORAGE_REGION"]
bucket = oss2.Bucket(
    oss2.Auth(os.environ["OBJECT_STORAGE_SECRET_ID"], os.environ["OBJECT_STORAGE_SECRET_KEY"]),
    f"https://{region}.aliyuncs.com",
    os.environ["OBJECT_STORAGE_BUCKET"],
)

for item in ITEMS:
    key = item["key"]
    validate_key(key)
    signed_url = bucket.sign_url("GET", key, EXPIRES)
    print(json.dumps({"key": key, "size": item["size"], "url": signed_url}, ensure_ascii=False), flush=True)
"""


def run_remote_python(script: str, *args: str, stdout=None) -> subprocess.CompletedProcess:
    cmd = [
        "ssh",
        "-i",
        str(KEY_PATH),
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=10",
        REMOTE,
        "cd",
        REMOTE_DIR,
        "&&",
        "docker",
        "compose",
        "exec",
        "-T",
        "api",
        "python",
        "-",
        *args,
    ]
    return subprocess.run(
        cmd,
        input=script,
        text=True,
        stdout=stdout if stdout is not None else subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def load_manifest(manifest_path: Path) -> list[dict]:
    if manifest_path.exists():
        return [json.loads(line) for line in manifest_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    result = run_remote_python(REMOTE_LIST_SCRIPT)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(result.stdout, encoding="utf-8")

    return [json.loads(line) for line in result.stdout.splitlines() if line.strip()]


def missing_items(manifest: list[dict]) -> list[dict]:
    missing = []
    for item in manifest:
        key = item["key"]
        size = int(item["size"])
        path = STORAGE_DIR / key
        if not path.exists() or path.stat().st_size != size:
            missing.append({"key": key, "size": size})
    return missing


def batched(items: list[dict], batch_size: int) -> list[list[dict]]:
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def sign_urls(items: list[dict]) -> list[dict]:
    script = REMOTE_SIGN_URLS_TEMPLATE.replace("__ITEMS_JSON__", json.dumps(items, ensure_ascii=False))
    result = run_remote_python(script)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    signed = []
    for line in result.stdout.splitlines():
        if line.strip():
            signed.append(json.loads(line))
    return signed


def download_signed_item(item: dict, timeout: int) -> tuple[str, int, str | None]:
    key = item["key"]
    size = int(item["size"])
    url = item["url"]
    ensure_safe_key(key)
    target = STORAGE_DIR / key
    tmp = target.with_suffix(target.suffix + ".part")
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response, tmp.open("wb") as handle:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
        actual = tmp.stat().st_size
        if actual != size:
            tmp.unlink(missing_ok=True)
            return key, 0, f"expected {size} bytes, got {actual}"
        tmp.replace(target)
        return key, size, None
    except Exception as exc:
        tmp.unlink(missing_ok=True)
        return key, 0, str(exc)


def direct_download_missing(
    manifest: list[dict],
    workers: int,
    batch_size: int,
    timeout: int,
    retries: int,
) -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    remaining = missing_items(manifest)
    total_bytes = sum(int(item["size"]) for item in remaining)
    print(f"missing={len(remaining)} total={total_bytes / 1024**3:.3f} GiB")
    if not remaining:
        return

    for attempt in range(1, retries + 1):
        failed: list[dict] = []
        done = 0
        done_bytes = 0
        started = time.monotonic()
        print(f"attempt={attempt} batches={len(batched(remaining, batch_size))} workers={workers}")
        for batch_index, batch in enumerate(batched(remaining, batch_size), 1):
            signed = sign_urls(batch)
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                futures = [executor.submit(download_signed_item, item, timeout) for item in signed]
                for future in concurrent.futures.as_completed(futures):
                    key, size, error = future.result()
                    if error:
                        failed.append({"key": key, "size": next(int(item["size"]) for item in batch if item["key"] == key)})
                    else:
                        done += 1
                        done_bytes += size
            elapsed = max(time.monotonic() - started, 0.001)
            print(
                f"batch={batch_index} done={done}/{len(remaining)} "
                f"downloaded={done_bytes / 1024**3:.3f} GiB "
                f"rate={done_bytes / 1024**2 / elapsed:.2f} MiB/s "
                f"failed={len(failed)}",
                flush=True,
            )

        if not failed:
            return
        remaining = failed
        print(f"retrying_failed={len(remaining)}", flush=True)

    if remaining:
        raise SystemExit(f"failed to download {len(remaining)} objects after {retries} attempts")


def mirror_remote_storage() -> None:
    result = run_remote_python(REMOTE_MIRROR_SCRIPT, stdout=None)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def rsync_storage() -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        "rsync",
        "-az",
        "--partial",
        "--info=progress2,stats2",
        "--human-readable",
        "-e",
        f"ssh -i {KEY_PATH}",
        f"{REMOTE}:{REMOTE_DIR}/storage/",
        f"{STORAGE_DIR}/",
    ]
    subprocess.run(cmd, check=True)


def ensure_safe_key(key: str) -> None:
    path = PurePosixPath(key)
    if key.startswith("/") or ".." in path.parts:
        raise ValueError(f"unsafe object key: {key}")


def stream_key_chunk(keys: list[str], worker_label: str) -> tuple[subprocess.Popen, subprocess.Popen]:
    for key in keys:
        ensure_safe_key(key)
        (STORAGE_DIR / key).parent.mkdir(parents=True, exist_ok=True)

    script = (
        REMOTE_TAR_STREAM_TEMPLATE
        .replace("__KEYS_JSON__", json.dumps(keys, ensure_ascii=False))
        .replace("__WORKER_LABEL__", worker_label)
    )
    ssh_cmd = [
        "ssh",
        "-i",
        str(KEY_PATH),
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=10",
        REMOTE,
        "cd",
        REMOTE_DIR,
        "&&",
        "docker",
        "compose",
        "exec",
        "-T",
        "api",
        "python",
        "-",
    ]
    tar_cmd = ["tar", "-xf", "-", "-C", str(STORAGE_DIR)]
    ssh = subprocess.Popen(ssh_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=False)
    assert ssh.stdin is not None
    assert ssh.stdout is not None
    tar = subprocess.Popen(tar_cmd, stdin=ssh.stdout)
    ssh.stdout.close()
    ssh.stdin.write(script.encode("utf-8"))
    ssh.stdin.close()
    return ssh, tar


def stream_missing_objects(manifest: list[dict], parallel_streams: int = 1) -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    missing = []
    missing_bytes = 0
    for item in manifest:
        key = item["key"]
        size = int(item["size"])
        path = STORAGE_DIR / key
        if not path.exists() or path.stat().st_size != size:
            missing.append(key)
            missing_bytes += size

    print(f"missing={len(missing)} total={missing_bytes / 1024**3:.3f} GiB")
    if not missing:
        return

    parallel_streams = max(1, parallel_streams)
    chunks = [missing[i::parallel_streams] for i in range(parallel_streams)]
    workers = []
    for idx, keys in enumerate(chunks, 1):
        if keys:
            workers.append((idx, *stream_key_chunk(keys, f"w{idx}")))

    exit_code = 0
    for idx, ssh, tar in workers:
        tar_return = tar.wait()
        ssh_return = ssh.wait()
        if tar_return != 0:
            print(f"worker w{idx} tar exited with {tar_return}")
            exit_code = tar_return
        if ssh_return != 0:
            print(f"worker w{idx} ssh exited with {ssh_return}")
            exit_code = ssh_return
    if exit_code:
        raise SystemExit(exit_code)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(ROOT / "backups" / "oss_manifest.jsonl"))
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--skip-remote-mirror", action="store_true")
    parser.add_argument("--skip-rsync", action="store_true")
    parser.add_argument("--stream-missing", action="store_true")
    parser.add_argument("--parallel-streams", type=int, default=1)
    parser.add_argument("--direct-download-missing", action="store_true")
    parser.add_argument("--direct-workers", type=int, default=16)
    parser.add_argument("--direct-batch-size", type=int, default=500)
    parser.add_argument("--direct-timeout", type=int, default=120)
    parser.add_argument("--direct-retries", type=int, default=3)
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    total_bytes = sum(int(item["size"]) for item in manifest)
    print(f"objects={len(manifest)} total={total_bytes / 1024**3:.3f} GiB")
    if args.manifest_only:
        return
    if args.stream_missing:
        stream_missing_objects(manifest, args.parallel_streams)
        return
    if args.direct_download_missing:
        direct_download_missing(
            manifest,
            workers=args.direct_workers,
            batch_size=args.direct_batch_size,
            timeout=args.direct_timeout,
            retries=args.direct_retries,
        )
        return
    if not args.skip_remote_mirror:
        mirror_remote_storage()
    if not args.skip_rsync:
        rsync_storage()


if __name__ == "__main__":
    main()
