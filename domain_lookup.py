#!/usr/bin/env python3
"""domain_lookup.py — Check whether a list of domain names resolves in DNS.

Reads a list of domains (built-in sample of 20 domains), resolves each one
via DNS-over-HTTPS (Google Public DNS, https://dns.google/resolve) with a
plain-socket fallback, and writes the results
(domain, resolved_ip_or_EMPTY, status) to domains_results.csv.

Usage:
    python3 domain_lookup.py
"""

import csv
import json
import socket
import urllib.request
from pathlib import Path

DOMAINS = [
    "google.com",
    "dawn.com",
    "propakistani.pk",
    "techjuice.pk",
    "techx.pk",
    "blogreach.com",
    "techabout.com",
    "hamariweb.com",
    "pakwired.com",
    "startuppakistan.com.pk",
    "github.com",
    "python.org",
    "kaggle.com",
    "wikipedia.org",
    "bbc.com",
    "fatimacooks.net",
    "pakistaneats.com",
    "foodofpakistan.com",
    "this-domain-should-not-resolve-xyz123.com",
    "another-fake-domain-abc999.net",
]

OUTPUT_CSV = Path(__file__).with_name("domains_results.csv")
DOH_URL = "https://dns.google/resolve?name={}&type=A"


def lookup_doh(domain: str, timeout: int = 8) -> tuple[str, str] | None:
    """Resolve via DNS-over-HTTPS. Returns (ip, status) or None on transport error."""
    try:
        req = urllib.request.Request(DOH_URL.format(domain), headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
        if data.get("Status") == 0 and data.get("Answer"):
            ips = [a["data"] for a in data["Answer"] if a.get("type") == 1]
            if ips:
                return ips[0], "RESOLVED"
        return "", "FAILED"
    except Exception:
        return None


def lookup(domain: str, timeout: int = 5) -> tuple[str, str]:
    """Return (ip, status) for a domain. Empty ip + 'FAILED' on error."""
    result = lookup_doh(domain)
    if result is not None:
        return result
    # Fallback: plain socket resolution
    socket.setdefaulttimeout(timeout)
    try:
        return socket.gethostbyname(domain), "RESOLVED"
    except (socket.gaierror, socket.timeout, OSError):
        return "", "FAILED"


def main() -> None:
    results = []
    for domain in DOMAINS:
        ip, status = lookup(domain)
        results.append({"domain": domain, "ip_address": ip, "status": status})
        print(f"{domain:45s} -> {ip or '-':18s} {status}")

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["domain", "ip_address", "status"])
        writer.writeheader()
        writer.writerows(results)

    resolved = sum(1 for r in results if r["status"] == "RESOLVED")
    print(f"\n{resolved}/{len(results)} domains resolved. Saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
