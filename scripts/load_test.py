#!/usr/bin/env python3
"""
🔥 Load Testing Script - 1000 Concurrent Users
==============================================

Simulates launch day traffic to verify system can handle load.

Target: 1000 concurrent users
Requirements:
- <200ms response time (p95)
- >99.5% success rate
- <0.1% error rate
- All endpoints functional

Author: Phoenix (Claude Thread 3)
Date: 2025-12-09
Phase: Launch Sprint v17.2 - Phase 4 Testing & QA
"""

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import httpx


@dataclass
class LoadTestConfig:
    """Load test configuration."""
    base_url: str = "https://helixspiral.work"  # Backend API
    concurrent_users: int = 1000
    requests_per_user: int = 10
    timeout: float = 30.0
    ramp_up_seconds: int = 10  # Gradual ramp to avoid thundering herd


@dataclass
class RequestResult:
    """Single request result."""
    endpoint: str
    status_code: int
    response_time: float
    success: bool
    error: Optional[str] = None


class LoadTester:
    """Load testing orchestrator."""

    def __init__(self, config: LoadTestConfig):
        self.config = config
        self.results: List[RequestResult] = []
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    async def make_request(self, client: httpx.AsyncClient, endpoint: str) -> RequestResult:
        """Make a single HTTP request and record result."""
        start = time.time()
        try:
            response = await client.get(f"{self.config.base_url}{endpoint}")
            elapsed = time.time() - start

            return RequestResult(
                endpoint=endpoint,
                status_code=response.status_code,
                response_time=elapsed,
                success=(200 <= response.status_code < 300)
            )
        except Exception as e:
            elapsed = time.time() - start
            return RequestResult(
                endpoint=endpoint,
                status_code=0,
                response_time=elapsed,
                success=False,
                error=str(e)
            )

    async def simulate_user(self, user_id: int, delay: float = 0) -> List[RequestResult]:
        """Simulate a single user making multiple requests."""
        # Stagger start times to ramp up gradually
        await asyncio.sleep(delay)

        endpoints = [
            "/health",
            "/api/claude/status",
            "/.well-known/helix.json",
            "/health",  # Hit health twice (common pattern)
        ]

        results = []
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            for endpoint in endpoints:
                result = await self.make_request(client, endpoint)
                results.append(result)
                # Small delay between requests (realistic user behavior)
                await asyncio.sleep(0.1)

        return results

    async def run_load_test(self) -> Dict:
        """Execute the load test with concurrent users."""
        print(f"🔥 Starting load test: {self.config.concurrent_users} concurrent users")
        print(f"📡 Target: {self.config.base_url}")
        print(f"⏱️  Ramp-up: {self.config.ramp_up_seconds}s")
        print("=" * 60)

        self.start_time = time.time()

        # Calculate delay between user spawns for gradual ramp-up
        delay_per_user = self.config.ramp_up_seconds / self.config.concurrent_users

        # Create tasks for all users
        tasks = [
            self.simulate_user(i, delay=i * delay_per_user)
            for i in range(self.config.concurrent_users)
        ]

        # Run all users concurrently
        print(f"🚀 Spawning {self.config.concurrent_users} users...")
        all_results = await asyncio.gather(*tasks, return_exceptions=True)

        self.end_time = time.time()

        # Flatten results
        for user_results in all_results:
            if isinstance(user_results, list):
                self.results.extend(user_results)

        # Generate report
        return self.generate_report()

    def generate_report(self) -> Dict:
        """Generate comprehensive test report."""
        if not self.results:
            return {"error": "No results collected"}

        total_requests = len(self.results)
        successful = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]

        response_times = [r.response_time for r in self.results]
        response_times.sort()

        # Calculate percentiles
        p50_idx = int(len(response_times) * 0.50)
        p95_idx = int(len(response_times) * 0.95)
        p99_idx = int(len(response_times) * 0.99)

        duration = self.end_time - self.start_time if self.start_time and self.end_time else 0

        report = {
            "summary": {
                "total_requests": total_requests,
                "successful": len(successful),
                "failed": len(failed),
                "success_rate": (len(successful) / total_requests * 100) if total_requests > 0 else 0,
                "error_rate": (len(failed) / total_requests * 100) if total_requests > 0 else 0,
                "duration_seconds": round(duration, 2),
                "requests_per_second": round(total_requests / duration, 2) if duration > 0 else 0,
            },
            "response_times": {
                "min": round(min(response_times) * 1000, 2) if response_times else 0,
                "max": round(max(response_times) * 1000, 2) if response_times else 0,
                "mean": round(sum(response_times) / len(response_times) * 1000, 2) if response_times else 0,
                "p50": round(response_times[p50_idx] * 1000, 2) if p50_idx < len(response_times) else 0,
                "p95": round(response_times[p95_idx] * 1000, 2) if p95_idx < len(response_times) else 0,
                "p99": round(response_times[p99_idx] * 1000, 2) if p99_idx < len(response_times) else 0,
                "unit": "ms"
            },
            "endpoints": self._analyze_endpoints(),
            "errors": self._analyze_errors(),
            "launch_readiness": self._check_launch_criteria()
        }

        return report

    def _analyze_endpoints(self) -> Dict:
        """Analyze results by endpoint."""
        endpoint_stats = {}
        for result in self.results:
            if result.endpoint not in endpoint_stats:
                endpoint_stats[result.endpoint] = {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "avg_response_time": 0,
                    "response_times": []
                }

            stats = endpoint_stats[result.endpoint]
            stats["total"] += 1
            if result.success:
                stats["successful"] += 1
            else:
                stats["failed"] += 1
            stats["response_times"].append(result.response_time)

        # Calculate averages
        for endpoint, stats in endpoint_stats.items():
            if stats["response_times"]:
                stats["avg_response_time"] = round(
                    sum(stats["response_times"]) / len(stats["response_times"]) * 1000, 2
                )
            stats["success_rate"] = round(
                (stats["successful"] / stats["total"] * 100) if stats["total"] > 0 else 0, 2
            )
            del stats["response_times"]  # Remove raw data from report

        return endpoint_stats

    def _analyze_errors(self) -> Dict:
        """Analyze error patterns."""
        error_counts = {}
        for result in self.results:
            if result.error:
                error_counts[result.error] = error_counts.get(result.error, 0) + 1
            elif not result.success:
                status_key = f"HTTP {result.status_code}"
                error_counts[status_key] = error_counts.get(status_key, 0) + 1

        return error_counts

    def _check_launch_criteria(self) -> Dict:
        """Check against launch readiness criteria."""
        response_times = [r.response_time for r in self.results]
        response_times.sort()
        p95_idx = int(len(response_times) * 0.95)
        p95_time = response_times[p95_idx] * 1000 if p95_idx < len(response_times) else 999

        success_rate = (len([r for r in self.results if r.success]) / len(self.results) * 100) if self.results else 0
        error_rate = 100 - success_rate

        criteria = {
            "p95_response_time": {
                "target": "<200ms",
                "actual": f"{p95_time:.2f}ms",
                "pass": p95_time < 200
            },
            "success_rate": {
                "target": ">99.5%",
                "actual": f"{success_rate:.2f}%",
                "pass": success_rate > 99.5
            },
            "error_rate": {
                "target": "<0.1%",
                "actual": f"{error_rate:.2f}%",
                "pass": error_rate < 0.1
            },
            "overall_pass": p95_time < 200 and success_rate > 99.5 and error_rate < 0.1
        }

        return criteria

    def print_report(self, report: Dict):
        """Pretty print the report."""
        print("\n" + "=" * 60)
        print("📊 LOAD TEST RESULTS")
        print("=" * 60)

        summary = report["summary"]
        print(f"\n📈 Summary:")
        print(f"  Total Requests: {summary['total_requests']}")
        print(f"  Successful: {summary['successful']} ({summary['success_rate']:.2f}%)")
        print(f"  Failed: {summary['failed']} ({summary['error_rate']:.2f}%)")
        print(f"  Duration: {summary['duration_seconds']}s")
        print(f"  RPS: {summary['requests_per_second']}")

        times = report["response_times"]
        print(f"\n⏱️  Response Times (ms):")
        print(f"  Min: {times['min']}")
        print(f"  Mean: {times['mean']}")
        print(f"  P50: {times['p50']}")
        print(f"  P95: {times['p95']}")
        print(f"  P99: {times['p99']}")
        print(f"  Max: {times['max']}")

        print(f"\n🎯 Endpoints:")
        for endpoint, stats in report["endpoints"].items():
            status = "✅" if stats["success_rate"] > 99 else "⚠️"
            print(f"  {status} {endpoint}")
            print(f"     Success: {stats['success_rate']}% | Avg: {stats['avg_response_time']}ms")

        if report["errors"]:
            print(f"\n❌ Errors:")
            for error, count in report["errors"].items():
                print(f"  {error}: {count} occurrences")

        criteria = report["launch_readiness"]
        print(f"\n🚀 Launch Readiness:")
        for key, check in criteria.items():
            if key == "overall_pass":
                continue
            status = "✅" if check["pass"] else "❌"
            print(f"  {status} {key}: {check['actual']} (target: {check['target']})")

        overall_status = "✅ READY FOR LAUNCH" if criteria["overall_pass"] else "⚠️ NEEDS IMPROVEMENT"
        print(f"\n{'=' * 60}")
        print(f"{overall_status}")
        print(f"{'=' * 60}\n")


async def main():
    """Run load test."""
    config = LoadTestConfig(
        base_url="https://helixspiral.work",  # Production API
        concurrent_users=1000,
        ramp_up_seconds=10
    )

    tester = LoadTester(config)

    try:
        report = await tester.run_load_test()
        tester.print_report(report)

        # Save report to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"load_test_report_{timestamp}.json"

        import json
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)

        print(f"📄 Report saved to: {filename}")

        # Exit code based on readiness
        if not report["launch_readiness"]["overall_pass"]:
            print("\n⚠️  System NOT ready for launch - review failures above")
            return 1

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Load test interrupted by user")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
