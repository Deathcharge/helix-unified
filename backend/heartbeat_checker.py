#!/usr/bin/env python3
"""
Helix Services Heartbeat Checker v1.0
======================================
Monitors all 7 Helix service endpoints for availability.
Can be run standalone or integrated with Discord bot for automated diagnostics.

Author: Andrew John Ward + Claude
Build: v1.0-heartbeat-checker
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import requests


def load_services_manifest() -> Dict[str, Any]:
    """Load services manifest from state directory."""
    manifest_path = Path(__file__).parent.parent / "Helix/state/services_manifest.json"

    if not manifest_path.exists():
        raise FileNotFoundError(f"Services manifest not found at {manifest_path}")

    with open(manifest_path, "r") as f:
        return json.load(f)


def check_service(url: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Check if a service is responding.

    Returns:
        Dict with status, ok flag, response time, and error if any
    """
    try:
        start = time.time()
        response = requests.get(url, timeout=timeout)
        elapsed = time.time() - start

        return {
            "status": response.status_code,
            "ok": response.ok,
            "response_time_ms": round(elapsed * 1000, 2),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "error": None
        }
    except requests.exceptions.Timeout:
        return {
            "status": None,
            "ok": False,
            "response_time_ms": None,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "error": "Timeout"
        }
    except requests.exceptions.ConnectionError as e:
        return {
            "status": None,
            "ok": False,
            "response_time_ms": None,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "error": f"Connection Error: {str(e)[:100]}"
        }
    except Exception as e:
        return {
            "status": None,
            "ok": False,
            "response_time_ms": None,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "error": f"Error: {str(e)[:100]}"
        }


def heartbeat() -> Dict[str, Any]:
    """
    Check all services and return results.
    Also logs to heartbeat_log.json for historical tracking.
    """
    manifest = load_services_manifest()
    services = manifest["services"]

    # Check all services
    results = {}
    for service_key, service_info in services.items():
        print(f"Checking {service_info['name']}...")
        results[service_key] = check_service(service_info["url"])

    # Create log entry
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "results": results,
        "summary": {
            "total": len(results),
            "ok": sum(1 for r in results.values() if r["ok"]),
            "failed": sum(1 for r in results.values() if not r["ok"])
        }
    }

    # Save to log file (keep last 20 entries)
    log_file = Path(__file__).parent.parent / "Helix/state/heartbeat_log.json"
    logs = []

    if log_file.exists():
        try:
            with open(log_file, "r") as f:
                logs = json.load(f)
        except Exception:
            logs = []

    logs.append(log_entry)
    logs = logs[-20:]  # Keep only last 20 heartbeats

    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)

    return log_entry


def print_heartbeat_summary(results: Dict[str, Any]) -> None:
    """Print a formatted summary of heartbeat results."""
    manifest = load_services_manifest()
    services = manifest["services"]

    print("\n" + "=" * 70)
    print(f"🧠 HELIX SERVICES HEARTBEAT - {results['timestamp']}")
    print("=" * 70)

    for service_key, result in results["results"].items():
        service_name = services[service_key]["name"]
        status_icon = "✅" if result["ok"] else "❌"
        status_code = result["status"] or "N/A"
        response_time = f"{result['response_time_ms']}ms" if result["response_time_ms"] else "N/A"

        print(f"{status_icon} {service_name:30s} → {status_code:>4} ({response_time})")

        if result["error"]:
            print(f"   Error: {result['error']}")

    print("\n" + "-" * 70)
    summary = results["summary"]
    print(f"Summary: {summary['ok']}/{summary['total']} services responding")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    print("🔍 Running Helix Services Heartbeat Check...\n")

    try:
        results = heartbeat()
        print_heartbeat_summary(results)

        # Exit with error code if any service is down
        if results["summary"]["failed"] > 0:
            exit(1)
        else:
            print("✅ All services operational!")
            exit(0)

    except Exception as e:
        print(f"❌ Heartbeat check failed: {e}")
        exit(2)
