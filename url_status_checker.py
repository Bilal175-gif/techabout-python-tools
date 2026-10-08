#!/usr/bin/env python3
"""URL Status Checker — check HTTP status of many URLs concurrently.

For each URL it reports:
  * HTTP status code (or ERROR if unreachable)
  * Final URL after following redirects
  * Response time in seconds

Usage:
    python url_status_checker.py https://example.com https://google.com
    python url_status_checker.py --file urls.txt
    python url_status_checker.py --file urls.txt --output results.csv

Only the Python standard library is used.
"""

import argparse
import csv
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

USER_AGENT = "url-status-checker/1.0"


def normalize_url(url):
    """Trim and add https:// when no scheme is present."""
    url = url.strip()
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def check_url(url, timeout):
    """Fetch one URL, return a result dict. Never raises."""
    target = normalize_url(url)
    start = time.perf_counter()
    try:
        req = urllib.request.Request(target, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status, final_url, error = resp.getcode(), resp.geturl(), ""
    except urllib.error.HTTPError as e:
        # HTTPError still carries the status code (404, 500, ...)
        status, final_url, error = e.code, target, ""
    except Exception as e:  # DNS failure, timeout, refused, SSL, ...
        status, final_url, error = "ERROR", target, type(e).__name__
    elapsed = round(time.perf_counter() - start, 2)
    return {
        "url": url.strip(),
        "status": status,
        "final_url": final_url,
        "time_s": elapsed,
        "error": error,
    }


def print_table(results, max_width=60):
    """Print results as an aligned plain-text table."""
    headers = ["URL", "Status", "Time (s)", "Final URL", "Error"]
    rows = [
        [r["url"], str(r["status"]), str(r["time_s"]), r["final_url"], r["error"]]
        for r in results
    ]

    def fit(text, width):
        text = str(text)
        return text if len(text) <= width else text[: width - 1] + "…"

    widths = []
    for i, h in enumerate(headers):
        col_max = max([len(h)] + [len(r[i]) for r in rows] or [len(h)])
        widths.append(min(col_max, max_width))

    def fmt(cells):
        return " | ".join(fit(c, w).ljust(w) for c, w in zip(cells, widths))

    print(fmt(headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(fmt(row))


def main():
    parser = argparse.ArgumentParser(
        description="Check HTTP status of URLs concurrently. Reports the "
                    "status code, final URL after redirects, and response "
                    "time for each URL.",
        epilog="Example: python url_status_checker.py --file urls.txt "
               "--output results.csv",
    )
    parser.add_argument("urls", nargs="*", help="URLs to check")
    parser.add_argument(
        "--file", "-f", default=None,
        help="Text file with one URL per line (blank lines and # comments ignored)",
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Save results to a CSV file",
    )
    parser.add_argument(
        "--workers", "-w", type=int, default=10,
        help="Number of concurrent workers (default: 10)",
    )
    parser.add_argument(
        "--timeout", "-t", type=float, default=15,
        help="Per-request timeout in seconds (default: 15)",
    )
    args = parser.parse_args()

    url_list = []
    if args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        url_list.append(line)
        except OSError as e:
            print(f"Error reading URL file: {e}", file=sys.stderr)
            return 1
    url_list.extend(u for u in args.urls if u.strip())
    url_list = list(dict.fromkeys(url_list))  # de-duplicate, keep order

    if not url_list:
        parser.error("No URLs given. Pass URLs as arguments or use --file.")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda u: check_url(u, args.timeout), url_list))

    print_table(results)

    ok = sum(1 for r in results if isinstance(r["status"], int) and 200 <= r["status"] < 400)
    failed = len(results) - ok
    print(f"\nChecked {len(results)} URL(s): {ok} OK, {failed} failed/error")

    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["url", "status", "final_url", "time_s", "error"]
            )
            writer.writeheader()
            writer.writerows(results)
        print(f"Saved: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
