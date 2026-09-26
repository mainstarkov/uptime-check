#!/usr/bin/env python3
"""Check HTTP endpoints and print a compact status report."""
import argparse
import json
import time
import urllib.error
import urllib.request

def check(url: str, timeout: float) -> dict:
    started = time.perf_counter()
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "uptime-check/1.0"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
        error = None
    except urllib.error.HTTPError as exc:
        status, error = exc.code, str(exc)
    except Exception as exc:
        status, error = 0, str(exc)
    elapsed = round((time.perf_counter() - started) * 1000)
    return {"url": url, "ok": 200 <= status < 400, "status": status, "ms": elapsed, "error": error}

def main() -> None:
    parser = argparse.ArgumentParser(description="Check websites from the terminal")
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--timeout", type=float, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = [check(url if "://" in url else f"https://{url}", args.timeout) for url in args.urls]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            mark = "OK" if item["ok"] else "FAIL"
            print(f"{mark:4} {item['status']:3} {item['ms']:5} ms  {item['url']}")
    raise SystemExit(0 if all(item["ok"] for item in results) else 1)

if __name__ == "__main__":
    main()
