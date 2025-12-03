#!/usr/bin/env python3
"""
Load Testing Script
===================

Test API performance under load using threading.
"""

import os
import time
import requests
import threading
import statistics
from datetime import datetime
from typing import List, Dict

API_URL = os.getenv("HELIX_API_URL", "http://localhost:8000")


class LoadTester:
    """Load testing class"""

    def __init__(self, url: str):
        self.url = url
        self.results: List[Dict] = []
        self.lock = threading.Lock()

    def single_request(self, endpoint: str, method: str = "GET", data: dict = None) -> Dict:
        """Make a single request and measure time"""
        start_time = time.time()

        try:
            if method == "GET":
                response = requests.get(f"{self.url}{endpoint}", timeout=10)
            elif method == "POST":
                response = requests.post(f"{self.url}{endpoint}", json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            elapsed = time.time() - start_time

            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "elapsed_ms": elapsed * 1000,
                "timestamp": datetime.now()
            }

        except Exception as e:
            elapsed = time.time() - start_time
            return {
                "success": False,
                "status_code": 0,
                "elapsed_ms": elapsed * 1000,
                "error": str(e),
                "timestamp": datetime.now()
            }

    def worker(self, endpoint: str, num_requests: int):
        """Worker thread that makes multiple requests"""
        for _ in range(num_requests):
            result = self.single_request(endpoint)

            with self.lock:
                self.results.append(result)

    def run_load_test(
        self,
        endpoint: str,
        total_requests: int = 100,
        concurrent_threads: int = 10
    ):
        """Run load test with multiple threads"""
        print(f"\n🔥 Load Testing: {endpoint}")
        print(f"Total Requests: {total_requests}")
        print(f"Concurrent Threads: {concurrent_threads}")
        print("-" * 50)

        self.results = []
        requests_per_thread = total_requests // concurrent_threads

        start_time = time.time()

        # Create and start threads
        threads = []
        for _ in range(concurrent_threads):
            thread = threading.Thread(
                target=self.worker,
                args=(endpoint, requests_per_thread)
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        total_time = time.time() - start_time

        # Analyze results
        self.print_results(total_time)

    def print_results(self, total_time: float):
        """Print test results"""
        if not self.results:
            print("❌ No results to analyze")
            return

        # Success rate
        successes = sum(1 for r in self.results if r["success"])
        success_rate = (successes / len(self.results)) * 100

        # Response times
        response_times = [r["elapsed_ms"] for r in self.results]
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        median_time = statistics.median(response_times)

        # Percentiles
        sorted_times = sorted(response_times)
        p95 = sorted_times[int(len(sorted_times) * 0.95)]
        p99 = sorted_times[int(len(sorted_times) * 0.99)]

        # Requests per second
        rps = len(self.results) / total_time

        # Print summary
        print("\n📊 Results:")
        print("-" * 50)
        print(f"Total Requests: {len(self.results)}")
        print(f"Successful: {successes} ({success_rate:.1f}%)")
        print(f"Failed: {len(self.results) - successes}")
        print(f"\nTotal Time: {total_time:.2f}s")
        print(f"Requests/sec: {rps:.2f}")
        print(f"\nResponse Times (ms):")
        print(f"  Min:    {min_time:.2f}")
        print(f"  Avg:    {avg_time:.2f}")
        print(f"  Median: {median_time:.2f}")
        print(f"  Max:    {max_time:.2f}")
        print(f"  p95:    {p95:.2f}")
        print(f"  p99:    {p99:.2f}")

        # Status code distribution
        status_codes = {}
        for result in self.results:
            code = result["status_code"]
            status_codes[code] = status_codes.get(code, 0) + 1

        print(f"\nStatus Codes:")
        for code, count in sorted(status_codes.items()):
            print(f"  {code}: {count}")


def test_health_endpoint():
    """Test health endpoint"""
    tester = LoadTester(API_URL)
    tester.run_load_test("/health", total_requests=100, concurrent_threads=10)


def test_agents_endpoint():
    """Test agents list endpoint"""
    tester = LoadTester(API_URL)
    tester.run_load_test("/agents", total_requests=50, concurrent_threads=5)


def test_consciousness_endpoint():
    """Test consciousness metrics endpoint"""
    tester = LoadTester(API_URL)
    tester.run_load_test("/consciousness/metrics", total_requests=50, concurrent_threads=5)


def stress_test():
    """Run stress test with high concurrency"""
    print("\n⚡ STRESS TEST")
    print("=" * 50)

    tester = LoadTester(API_URL)
    tester.run_load_test("/health", total_requests=1000, concurrent_threads=50)


def main():
    """Main function"""
    print("\n" + "=" * 50)
    print("🌀 Helix Unified - Load Testing")
    print("=" * 50)
    print(f"Target: {API_URL}")

    # Test different endpoints
    test_health_endpoint()

    print("\n" + "=" * 50)
    test_agents_endpoint()

    print("\n" + "=" * 50)
    test_consciousness_endpoint()

    # Stress test
    choice = input("\n\nRun stress test (1000 requests)? (y/N): ")
    if choice.lower() == 'y':
        stress_test()

    print("\n" + "=" * 50)
    print("✅ Load testing complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
